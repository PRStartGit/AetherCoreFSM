import { Component, Input, Output, EventEmitter, OnInit, ViewChild, ElementRef, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-video-player',
  templateUrl: './video-player.component.html',
  styleUrls: ['./video-player.component.css']
})
export class VideoPlayerComponent implements OnInit, OnDestroy {
  @ViewChild('videoElement', { static: true }) videoElementRef!: ElementRef<HTMLVideoElement>;

  @Input() videoUrl: string = '';
  @Input() startPosition: number = 0;

  @Output() videoReady = new EventEmitter<HTMLVideoElement>();
  @Output() timeUpdate = new EventEmitter<number>();
  @Output() videoEnded = new EventEmitter<void>();

  isPlaying = false;
  currentTime = 0;
  duration = 0;
  volume = 1;
  isMuted = false;
  isFullscreen = false;
  showControls = true;
  controlsTimeout: any;

  ngOnInit(): void {
    const video = this.videoElementRef.nativeElement;

    video.addEventListener('loadedmetadata', () => {
      this.duration = video.duration;
      if (this.startPosition > 0 && this.startPosition < video.duration) {
        video.currentTime = this.startPosition;
      }
      this.videoReady.emit(video);
    });

    video.addEventListener('timeupdate', () => {
      this.currentTime = video.currentTime;
      this.timeUpdate.emit(video.currentTime);
    });

    video.addEventListener('ended', () => {
      this.isPlaying = false;
      this.videoEnded.emit();
    });

    video.addEventListener('play', () => {
      this.isPlaying = true;
    });

    video.addEventListener('pause', () => {
      this.isPlaying = false;
    });

    video.addEventListener('volumechange', () => {
      this.volume = video.volume;
      this.isMuted = video.muted;
    });
  }

  ngOnDestroy(): void {
    if (this.controlsTimeout) {
      clearTimeout(this.controlsTimeout);
    }
  }

  togglePlay(): void {
    const video = this.videoElementRef.nativeElement;
    if (video.paused) {
      video.play();
    } else {
      video.pause();
    }
  }

  seek(event: Event): void {
    const input = event.target as HTMLInputElement;
    const video = this.videoElementRef.nativeElement;
    video.currentTime = parseFloat(input.value);
  }

  setVolume(event: Event): void {
    const input = event.target as HTMLInputElement;
    const video = this.videoElementRef.nativeElement;
    video.volume = parseFloat(input.value);
  }

  toggleMute(): void {
    const video = this.videoElementRef.nativeElement;
    video.muted = !video.muted;
  }

  toggleFullscreen(): void {
    const container = this.videoElementRef.nativeElement.parentElement;
    if (!container) return;

    if (!document.fullscreenElement) {
      container.requestFullscreen().then(() => {
        this.isFullscreen = true;
      }).catch(err => {
        console.error('Error attempting to enable fullscreen:', err);
      });
    } else {
      document.exitFullscreen().then(() => {
        this.isFullscreen = false;
      });
    }
  }

  skipBackward(): void {
    const video = this.videoElementRef.nativeElement;
    video.currentTime = Math.max(0, video.currentTime - 10);
  }

  skipForward(): void {
    const video = this.videoElementRef.nativeElement;
    video.currentTime = Math.min(video.duration, video.currentTime + 10);
  }

  onMouseMove(): void {
    this.showControls = true;
    if (this.controlsTimeout) {
      clearTimeout(this.controlsTimeout);
    }
    this.controlsTimeout = setTimeout(() => {
      if (this.isPlaying) {
        this.showControls = false;
      }
    }, 3000);
  }

  formatTime(seconds: number): string {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  get progress(): number {
    return this.duration > 0 ? (this.currentTime / this.duration) * 100 : 0;
  }
}
