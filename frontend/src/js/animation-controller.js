/**
 * Animation Controller Module
 * Handles flight animation playback, speed control, and progress tracking
 */

class AnimationController {
    constructor(mapManager, onUpdate) {
        this.mapManager = mapManager;
        this.onUpdate = onUpdate; // Callback function for updates
        
        this.flightData = null;
        this.currentIndex = 0;
        this.isPlaying = false;
        this.speed = 1;
        this.animationFrameId = null;
    }

    /**
     * Set flight data
     * @param {Object} data - Flight data object
     */
    setFlightData(data) {
        this.flightData = data;
        this.currentIndex = 0;
    }

    /**
     * Start animation
     */
    play() {
        if (!this.flightData || this.isPlaying) return;
        
        this.isPlaying = true;
        this.animate();
    }

    /**
     * Pause animation
     */
    pause() {
        this.isPlaying = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    /**
     * Reset animation to start
     */
    reset() {
        this.pause();
        this.currentIndex = 0;
        this.updatePosition();
    }

    /**
     * Set animation speed
     * @param {number} speed - Speed multiplier
     */
    setSpeed(speed) {
        this.speed = speed;
    }

    /**
     * Seek to specific position
     * @param {number} progress - Progress percentage (0-100)
     */
    seek(progress) {
        if (!this.flightData) return;
        
        this.currentIndex = Math.floor((progress / 100) * (this.flightData.flightPoints.length - 1));
        this.updatePosition();
    }

    /**
     * Animation loop
     */
    animate() {
        if (!this.isPlaying || !this.flightData) return;
        
        this.currentIndex += this.speed;
        
        if (this.currentIndex >= this.flightData.flightPoints.length) {
            this.currentIndex = this.flightData.flightPoints.length - 1;
            this.pause();
            if (this.onUpdate) {
                this.onUpdate({
                    index: this.currentIndex,
                    progress: 100,
                    isPlaying: false
                });
            }
            return;
        }
        
        this.updatePosition();
        this.animationFrameId = requestAnimationFrame(() => this.animate());
    }

    /**
     * Update aircraft position on map
     */
    updatePosition() {
        if (!this.flightData) return;
        
        const index = Math.floor(this.currentIndex);
        const point = this.flightData.flightPoints[index];
        
        if (!point) return;
        
        // Update map
        this.mapManager.updateAircraftPosition(
            point.latitude,
            point.longitude,
            point.heading
        );
        
        // Update progress path
        const fullPath = this.flightData.flightPoints.map(p => [p.latitude, p.longitude]);
        this.mapManager.updateProgressPath(fullPath, index);
        
        // Call update callback
        if (this.onUpdate) {
            const progress = (this.currentIndex / (this.flightData.flightPoints.length - 1)) * 100;
            this.onUpdate({
                index: this.currentIndex,
                progress: progress,
                isPlaying: this.isPlaying,
                point: point
            });
        }
    }

    /**
     * Get current state
     * @returns {Object} Current animation state
     */
    getState() {
        return {
            currentIndex: this.currentIndex,
            isPlaying: this.isPlaying,
            speed: this.speed,
            progress: this.flightData ? 
                (this.currentIndex / (this.flightData.flightPoints.length - 1)) * 100 : 0
        };
    }

    /**
     * Cleanup
     */
    destroy() {
        this.pause();
        this.flightData = null;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AnimationController };
}