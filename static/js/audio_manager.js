class AudioManager {
    constructor(playback_rate = 1.25, playback_volume = 1.0) {
        this.audio_context = new (window.AudioContext || window.webkitAudioContext)();
        this.audio_queue = [];
        this.is_playing = false;
        this.playback_rate = playback_rate;
        this.playback_volume = playback_volume;
    }

    play_next_queue() {
        if (this.audio_queue.length === 0) {
            this.is_playing = false;
            return;
        }

        this.is_playing = true;
        const buffer = this.audio_queue.shift();
        const source = this.audio_context.createBufferSource();
        source.buffer = buffer;
        source.playbackRate.value = this.playback_rate;
        source.connect(this.audio_context.destination);

        source.onended = () => this.play_next_queue();
        source.start(0);
    }

    async add_to_queue(data) {
        const buffer = await this.audio_context.decodeAudioData(data);
        this.audio_queue.push(buffer);
    }

    play_audio(data) {
        await this.add_to_queue(data);
        if (!this.is_playing) {
            this.play_next_queue();
        }
    }

    stop_audio() {
        this.audio_context.suspend();
        this.audio_queue = [];
        this.is_playing = false;
        this.audio_context.resume();
    }
}

