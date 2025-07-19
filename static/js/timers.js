(function(){
    // Timer state stored in localStorage under 'taskCountdownTimers'
    let timers = {};
    let runner = null;

    function loadTimers(){
        const saved = localStorage.getItem('taskCountdownTimers');
        timers = saved ? JSON.parse(saved) : {};
    }

    function saveTimers(){
        localStorage.setItem('taskCountdownTimers', JSON.stringify(timers));
    }

    function formatTime(seconds){
        const h = String(Math.floor(seconds / 3600)).padStart(2,'0');
        const m = String(Math.floor((seconds % 3600) / 60)).padStart(2,'0');
        const s = String(seconds % 60).padStart(2,'0');
        return `${h}:${m}:${s}`;
    }

    function updateDisplay(taskId){
        const display = document.getElementById(`timer-display-${taskId}`);
        const overtimeEl = document.getElementById(`overtime-display-${taskId}`);
        if(!display) return;
        const t = timers[taskId] || {};
        const remaining = t.remainingSeconds || 0;
        const overtime = t.overtimeSeconds || 0;
        if(remaining > 0){
            display.textContent = `Time Remaining: ${formatTime(remaining)}`;
            display.classList?.remove('expired');
            if(overtimeEl) overtimeEl.style.display = 'none';
        } else {
            display.textContent = 'Time Remaining: 00:00:00';
            display.classList?.add('expired');
            if(overtimeEl){
                overtimeEl.style.display = 'block';
                overtimeEl.textContent = `Overtime: ${formatTime(overtime)}`;
            }
        }
    }

    function updateAllDisplays(){
        for(const id in timers){
            updateDisplay(id);
        }
    }

    function tick(){
        for(const id in timers){
            const t = timers[id];
            if(t.running){
                if(t.remainingSeconds > 0){
                    t.remainingSeconds--;
                    if(t.remainingSeconds === 0){
                        alert(`Time's up for task ${id}!`);
                    }
                } else {
                    t.overtimeSeconds = (t.overtimeSeconds || 0) + 1;
                }
            }
        }
        updateAllDisplays();
        saveTimers();
        // Dispatch event so other scripts (like dashboard) can react
        document.dispatchEvent(new Event('timersUpdated'));
    }

    function startRunner(){
        if(runner === null){
            runner = setInterval(tick, 1000);
        }
    }

    // Exposed API
    window.startTimer = function(taskId, estSeconds){
        loadTimers();
        if(!timers[taskId]){
            timers[taskId] = {remainingSeconds: estSeconds, overtimeSeconds:0, running:false};
        }
        if(timers[taskId].remainingSeconds <= 0){
            timers[taskId].remainingSeconds = estSeconds;
            timers[taskId].overtimeSeconds = 0;
        }
        timers[taskId].running = true;
        saveTimers();
    };

    window.pauseTimer = function(taskId){
        loadTimers();
        if(timers[taskId]){
            timers[taskId].running = false;
            saveTimers();
        }
    };

    window.stopTimer = function(taskId, estSeconds){
        loadTimers();
        timers[taskId] = {remainingSeconds: estSeconds, overtimeSeconds:0, running:false};
        saveTimers();
        updateDisplay(taskId);
    };

    window.loadTimers = function(){
        loadTimers();
        return timers;
    };

    document.addEventListener('DOMContentLoaded', function(){
        loadTimers();
        updateAllDisplays();
        startRunner();
    });
})();
