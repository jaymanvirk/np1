class AudioManager {
    constructor(playback_rate = 1.25, playback_volume = 1.0) {
        this.audio_context = new (window.AudioContext || window.webkitAudioContext)();
        this.audio_queue = [];
        this.is_playing = false;
        this.playback_rate = playback_rate;
        this.playback_volume = playback_volume;
        this.current_source = null;
    }

    async play_next_queue() {
        if (this.audio_queue.length === 0) {
            this.is_playing = false;
            return;
        }

        this.is_playing = true;
        const buffer = this.audio_queue.shift();
        this.current_source = this.audio_context.createBufferSource();
        this.current_source.buffer = buffer;
        this.current_source.playbackRate.value = this.playback_rate;
        this.current_source.connect(this.audio_context.destination);

        this.current_source.onended = () => this.play_next_queue();
        this.current_source.start(0);
    }

    async add_to_queue(data) {
        try {
            const buffer = await this.audio_context.decodeAudioData(data);
            this.audio_queue.push(buffer);
        } catch (error) {
            console.error('Error decoding audio data:', error);
        }
    }

    async play_audio(data) {
        await this.add_to_queue(data);
        if (!this.is_playing) {
            this.play_next_queue();
        }
    }

    stop_audio() {
        if (this.current_source) {
            this.current_source.stop();
        }
        this.audio_queue = [];
        this.is_playing = false;
    }
}

