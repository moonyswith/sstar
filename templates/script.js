const BACKEND_URL = '/api';

const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const trackList = document.getElementById('trackList');
const audioPlayer = document.getElementById('audioPlayer');
const centerPlayBtn = document.getElementById('centerPlayBtn');
const playIcon = document.getElementById('playIcon');
const vinylContainer = document.querySelector('.vinyl-container');
const playerImg = document.getElementById('playerImg');
const defaultVinyl = document.getElementById('defaultVinyl');
const playerTitle = document.getElementById('playerTitle');
const playerArtist = document.getElementById('playerArtist');

// Кнопки из вашего дизайна
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const loopBtn = document.getElementById('loopBtn');

let currentTrackList = []; // Храним список найденных треков для переключения
let currentTrackIndex = -1;
let isLooping = false;

searchButton.addEventListener('click', searchTracks);
searchInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') searchTracks(); });

async function searchTracks() {
    const query = searchInput.value.trim();
    if (!query) return;

    trackList.innerHTML = '<p style="text-align:center; color:#888; font-size:12px; padding:10px;">Поиск треков...</p>';
    trackList.classList.add('visible');

    try {
        const response = await fetch(`${BACKEND_URL}/search?q=${encodeURIComponent(query)}`);
        const tracks = await response.json();

        trackList.innerHTML = '';
        if (tracks.error) {
            trackList.innerHTML = `<p style="color:red; text-align:center; padding:10px;">${tracks.error}</p>`;
            return;
        }

        currentTrackList = tracks; // Запоминаем очередь для кнопок «Вперед/Назад»

        tracks.forEach((track, index) => {
            const card = document.createElement('div');
            card.className = 'track-card';
            card.addEventListener('click', () => playTrack(track, index));

            card.innerHTML = `
                <img src="${track.thumbnail}" alt="Cover">
                <div class="track-info">
                    <div class="track-title">${track.title}</div>
                    <div class="track-artist">${track.artist}</div>
                </div>
            `;
            trackList.appendChild(card);
        });
    } catch (err) {
        trackList.innerHTML = '<p style="color:red; text-align:center; padding:10px;">Ошибка сервера.</p>';
    }
}

async function playTrack(track, index) {
    trackList.classList.remove('visible');
    currentTrackIndex = index;

    defaultVinyl.style.display = 'none';
    playerImg.src = track.thumbnail;
    playerImg.style.display = 'block';

    playerTitle.innerText = track.title;
    playerArtist.innerText = track.artist;

    audioPlayer.src = '';
    setPlayingState(false);

    try {
        const response = await fetch(`${BACKEND_URL}/stream?id=${track.id}`);
        const data = await response.json();

        if (data.stream_url) {
            audioPlayer.src = data.stream_url;
            audioPlayer.play();
            setPlayingState(true);
        } else {
            alert('Не удалось загрузить поток.');
        }
    } catch (err) {
        alert('Ошибка сети при загрузке аудио.');
    }
}

// Кнопка Play/Pause по центру диска
centerPlayBtn.addEventListener('click', () => {
    if (!audioPlayer.src) return;
    if (audioPlayer.paused) {
        audioPlayer.play();
        setPlayingState(true);
    } else {
        audioPlayer.pause();
        setPlayingState(false);
    }
});

// Кнопка переключения Вперед
nextBtn.addEventListener('click', () => {
    if (currentTrackList.length > 0 && currentTrackIndex < currentTrackList.length - 1) {
        playTrack(currentTrackList[currentTrackIndex + 1], currentTrackIndex + 1);
    }
});

// Кнопка переключения Назад
prevBtn.addEventListener('click', () => {
    if (currentTrackList.length > 0 && currentTrackIndex > 0) {
        playTrack(currentTrackList[currentTrackIndex - 1], currentTrackIndex - 1);
    }
});

// Кнопка повтора трека (Loop) из дизайна
loopBtn.addEventListener('click', () => {
    isLooping = !isLooping;
    audioPlayer.loop = isLooping;
    loopBtn.classList.toggle('active', isLooping);
});

// Когда трек заканчивается самостоятельно
audioPlayer.addEventListener('ended', () => {
    if (!isLooping) {
        // Если повтор выключен, автоматически включаем следующий трек из поиска
        nextBtn.click();
    }
});

function setPlayingState(isPlaying) {
    if (isPlaying) {
        playIcon.classList.add('pause');
        vinylContainer.classList.add('playing');
    } else {
        playIcon.classList.remove('pause');
        vinylContainer.classList.remove('playing');
    }
}
