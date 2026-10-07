document.addEventListener('DOMContentLoaded', async function () {
    const lecteur = document.getElementById('lecteur');

    lecteur.src = `https://www.youtube.com/embed/${video_youtube_id}?enablejsapi=1`;

    const tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
});

function hideLoader() {
    const loaderContainer = document.getElementById('loader-container')
    const iframe = document.getElementById('lecteur')
    loaderContainer.style.display = 'none'
    iframe.style.display = 'block'
}

function getQuestionByTimecode(timecode) {
    return document.querySelector(`[data-timecode="${timecode}"]`);
}

let player;

function onPlayerStateChange(event) {
}

function onYouTubeIframeAPIReady() {
    player = new YT.Player('lecteur', {
        height: '450',
        width: '800',
        videoId: video_youtube_id,
        events: {
            onReady: hideLoader(),
            onStateChange: onPlayerStateChange,
        },
        playerVars: {
            rel: 0,
        },
    });
}


async function loadSimilarQuestions(question_id) {
    const apiURL = `/api/question/${question_id}?format=json`;
    return fetch(apiURL)
        .then(async (response) => {
            const json = await response.json();
            return json;
        });
}

async function updateCurrentQuestionInfos(timecode) {
    const currentQuestion = getQuestionByTimecode(timecode);

    if (currentQuestion.classList.contains('current')) {
        return;
    } else {
        document.querySelector('.current')?.classList.remove('current');
        currentQuestion.classList.add('current');
    }

    let similarQuestions = loadSimilarQuestions(currentQuestion.dataset.questionId).then(
        (data) => {
            if (data.length === 0) {
                document.querySelector('#similarQuestions').style.display = 'none';
                return;
            } else {
                document.querySelector('#similarQuestions').style.display = 'block';
                document.querySelector('#similarQuestions ul').innerHTML = '';
            }
            for (let similarQuestion of data) {
                const similarQuestionElement = document.createElement('li');
                similarQuestionElement.innerHTML = `<a href="/video/${similarQuestion.video}?timecode=${similarQuestion.timecode}">${similarQuestion.title} <i class="fa-solid fa-arrow-right"></i> ${similarQuestion.artist}</a>`;
                similarQuestionElement.classList.add('similarQuestion', 'list-group-item', 'input-group');
                document.querySelector('#similarQuestions ul').appendChild(similarQuestionElement);
            }
        }
    );


    const question = questions[timecode];
    document.querySelector('#currentQuestionInfos .title').textContent = question.title;
    document.querySelector('#currentQuestionInfos .answer').textContent = question.answer.content;
    document.querySelector('#currentQuestionInfos .artist').textContent = question.answer.artist;

    scrollToQuestion(timecode);
}

function goNextQuestion() {
    const timecodes = Object.keys(questions).map(Number);
    const nextTimecode = timecodes.find(timecode => timecode > player.getCurrentTime());
    if (nextTimecode) {
        goToQuestion(nextTimecode);
    }
}

function goPrevQuestion() {
    const timecodes = Object.keys(questions).map(Number);
    const previousTimecode = timecodes.reverse().find(timecode => timecode < document.querySelector('.current').dataset.timecode);
    if (previousTimecode !== undefined) {
        goToQuestion(previousTimecode);
    }
}