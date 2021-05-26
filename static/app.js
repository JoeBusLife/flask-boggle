const BASE_URL = "http://127.0.0.1:5000";
const $gameStart = $("#game-start")
const $countDown = $("#count-down")
const $guessForm = $("#guess-form")
const $guess = $("#guess")
const $showGuessResult = $("#show-guess-result")
const $score = $("#score")
const $highScore = $("#high-score")

let currentGame = null

class Game {
	constructor(){
		this.gameOver = false;
		this.score = 0;
		this.countDown = 60;
		this.corrGuesses = new Set();

		this.startTimer();
	}

	async checkGuess(guess) {
		const guessRes = await axios.post(`${BASE_URL}/guess`, {guess: guess});
		return guessRes.data.result;
	}

	startTimer(){
		//add timer to dom
		let timer = setInterval(function(){
			
			this.countDown -= 1;
			$countDown.html(this.countDown);

			if(this.countDown <= 0){
				this.handleGameOver()
				clearInterval(timer);
			}
		}.bind(this), 1000);
	}

	handleGameOver(){
		this.gameOver = true;
		axios.post(`${BASE_URL}/game/over`, {score: this.score});
		this.updateGameInfo();
	}

	// When game ends show ending message and update High Score in DOM
	updateGameInfo(){
		let msg = "Game Over"
		if(this.score > $highScore.html()){
			msg = "New High Score!";
			$highScore.html(this.score)
		}else if(this.score == $highScore.html()){
			msg = "Tied High Score";
		}
		$showGuessResult.html(msg)
	}
	
	// If the word hasn't already been guessed add it to set of guesses and add length of word to score
	addScore(corrWord){
		if(!this.corrGuesses.has(corrWord)){
			this.corrGuesses.add(corrWord);
			this.score += corrWord.length;
			
			return true
		}
		return false
	}
}

function startGame(){
	if (window.location.href.indexOf("game") > -1) {
    currentGame = new Game();
	}
}

$(window).on("load", startGame);


async function handleGuess(evt) {
	evt.preventDefault();

	if(currentGame.gameOver){
		$showGuessResult.html("Times Up!")
		return
	}

	const guess = $guess.val().toLowerCase();
	evt.target.reset();

	if(guess.length < 3){
		$showGuessResult.html("Word To Short!")
		return
	}

	let guessResText = await currentGame.checkGuess(guess);
	
	if(guessResText == "You got one!"){
		guessResText = !currentGame.addScore(guess) ? "Already got it!" : guessResText;
	}
	$score.html(currentGame.score)
	$showGuessResult.html(guessResText)
}

$guessForm.on("submit", handleGuess);