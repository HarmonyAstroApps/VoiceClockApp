document.addEventListener('DOMContentLoaded', function() {
    const showcase = document.querySelector('.screenshot-showcase');
    const track = document.querySelector('.screenshot-track');
    let isDragging = false;
    let startPosition = 0;
    let currentTranslate = 0;
    let previousTranslate = 0;
    let animationID = null;
    let isAnimating = true;
    const scrollSpeed = 1; // Constant scroll speed

    // Remove any existing animation
    track.style.animation = 'none';

    // Calculate the total width of the track content
    const calculateTrackWidth = () => {
        const trackItems = track.children;
        let totalWidth = 0;
        for (let item of trackItems) {
            totalWidth += item.offsetWidth;
        }
        return totalWidth;
    };

    // Function to handle continuous scrolling
    function animate() {
        if (isAnimating && !isDragging) {
            currentTranslate -= scrollSpeed;
            
            // Reset position when reaching the end
            const trackWidth = calculateTrackWidth();
            if (Math.abs(currentTranslate) >= trackWidth / 2) {
                currentTranslate = 0;
            }
            
            previousTranslate = currentTranslate;
            setSliderPosition();
        }
        
        // Only request new frame if animation is still running
        if (isAnimating && !isDragging) {
            animationID = requestAnimationFrame(animate);
        }
    }

    function touchStart(event) {
        if (event.type === 'touchstart') {
            event.preventDefault();
        }
        
        isAnimating = false;
        startPosition = getPositionX(event);
        isDragging = true;
        showcase.classList.add('grabbing');
        
        // Cancel any existing animation
        if (animationID !== null) {
            cancelAnimationFrame(animationID);
            animationID = null;
        }
    }

    function touchMove(event) {
        if (!isDragging) return;
        
        event.preventDefault();
        const currentPosition = getPositionX(event);
        const diff = currentPosition - startPosition;
        currentTranslate = previousTranslate + diff;
        setSliderPosition();
    }

    function touchEnd() {
        isDragging = false;
        showcase.classList.remove('grabbing');
        previousTranslate = currentTranslate;
        
        // Only resume animation if not hovering and not already animating
        if (!showcase.matches(':hover') && !isAnimating) {
            isAnimating = true;
            animationID = requestAnimationFrame(animate);
        }
    }

    function getPositionX(event) {
        return event.type.includes('mouse') 
            ? event.pageX 
            : event.touches[0].clientX;
    }

    function setSliderPosition() {
        track.style.transform = `translateX(${currentTranslate}px)`;
    }

    // Mouse events
    showcase.addEventListener('mousedown', touchStart);
    showcase.addEventListener('mousemove', touchMove);
    showcase.addEventListener('mouseup', touchEnd);
    showcase.addEventListener('mouseleave', touchEnd);

    // Touch events
    showcase.addEventListener('touchstart', touchStart, { passive: false });
    showcase.addEventListener('touchmove', touchMove, { passive: false });
    showcase.addEventListener('touchend', touchEnd);
    showcase.addEventListener('touchcancel', touchEnd);

    // Prevent context menu
    showcase.addEventListener('contextmenu', e => e.preventDefault());

    // Stop animation on hover
    showcase.addEventListener('mouseenter', () => {
        isAnimating = false;
        if (animationID !== null) {
            cancelAnimationFrame(animationID);
            animationID = null;
        }
    });

    // Resume animation when not dragging
    showcase.addEventListener('mouseleave', () => {
        if (!isDragging && !isAnimating) {
            isAnimating = true;
            animationID = requestAnimationFrame(animate);
        }
    });

    // Start initial animation
    animationID = requestAnimationFrame(animate);
});