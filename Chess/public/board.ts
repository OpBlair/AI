//chess board columns
const COLUMNS: string[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

//Square colors
const lightSquare: string = 'bg-yellow-50'; //soft cream
const darkSquare: string = 'bg-amber-700'; //warm chocolate

//State and Constants for Interaction
let selectedSquare: HTMLElement | null = null;
const highLightClass = 'ring-2 ring-blue-500 ring-inset';

//Initial Board State
const boardState: Record<string, string | null > = {
	'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br',
	'a7': 'bp', 'b7': 'bp', 'c7': 'bp', 'd7': 'bp', 'e7': 'bp', 'f7': 'bp', 'g7': 'bp', 'h7': 'bp',
	'a2': 'wp', 'b2': 'wp', 'c2': 'wp', 'd2': 'wp', 'e2': 'wp', 'f2': 'wp', 'g2': 'wp', 'h2': 'wp',
	'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
}

//path mapping
const pieceSVGMap: Record<string, string> = {
	'br': './assets/rookDark.svg',
	'bn': './assets/knightDark.svg',
	'bb': './assets/bishopDark.svg',
	'bq': './assets/queenDark.svg',
	'bk': './assets/kingDark.svg',
	'bp': './assets/pawnDark.svg',
	'wr': './assets/rookWhite.svg',
	'wn': './assets/knightWhite.svg',
	'wb': './assets/bishopWhite.svg',
	'wq': './assets/queenWhite.svg',
	'wk': './assets/kingWhite.svg',
	'wp': './assets/pawnWhite.svg',
}

//function to place a piece in a square
function renderPiece(square: HTMLElement, pieceCode: string | null): void{
	if(pieceCode && pieceSVGMap[pieceCode]){
		const svgPath = pieceSVGMap[pieceCode];
		square.innerHTML = `<img src="${svgPath}" alt="${pieceCode}" class="w-10/12 h-10/12 object-contain">`;
	}else{
		square.innerHTML = ''; //clear the square
	}
}

//generating the board
function createBoard(): void{
	const board = document.getElementById('chess-board') as HTMLElement;

	board.innerHTML = '' // clear existing squares

	for(let row = 8; row >=1; row--){
		for(let colIndex = 0; colIndex < 8; colIndex++){
			const col = COLUMNS[colIndex];
			const squareId = `${col}${row}`;
			const isDarkSquare = (row + colIndex) % 2 === 0;
			const bgColor = isDarkSquare ? darkSquare : lightSquare ;

			const square = document.createElement('div');
			square.id = squareId;
			square.dataset.row = row.toString();
			square.dataset.col = col;

			square.className = `
			    w-full aspect-square flex items-center justify-center
			    ${bgColor} rounded-sm shadow-inner
			    transition duration-200 ease-in-out
			    hover:ring-2 hover:ring-blue-400 cursor-pointer hover:ring-inset
			`;

			const pieceCode = boardState[squareId]; //use boardState
			renderPiece(square, pieceCode);// render the piece initially
			
			board.appendChild(square);
		}
	}
	console.log("Chessbaord and initial pieces generated successfully!");
}

//helper function to split the class string into an array of arguments
const getHighListClasses = () => highLightClass.split(' ');

//handle clicks on any square
function handleSquareClick(event: Event): void{
	//define element that received the click event
	const clickedElement = event.target as HTMLElement;

	//determine the actual square
	const square = clickedElement.closest('[data-row]') as HTMLElement | null;

	if(!square) return;
	const highLightClasses = getHighListClasses();

	//deselect the old square
	if(selectedSquare){
		selectedSquare.classList.remove(...highLightClasses);
	}

	//select the new square
	//first check if squre is already selected to allow deselection
	if(selectedSquare){
		//check for deselection.
		if(selectedSquare.id === square.id){
		//double-click or click same square deselects it
		selectedSquare = null;
		console.log(`Square deselected: ${square.id}.`);
		return;
		}

		//Move piece Logic (No validation yet)
		const fromSquareId = selectedSquare.id;
		const toSquareId = square.id;
		const pieceCode = boardState[fromSquareId];

		if(pieceCode){
			//update the state
			boardState[toSquareId] = pieceCode;
			boardState[fromSquareId] = null;

			//update the DOM
			renderPiece(square, pieceCode);
			renderPiece(selectedSquare, null);
			console.log(`Moved ${pieceCode} from ${fromSquareId} to ${toSquareId}`);
		}

		selectedSquare = null; //clear selection after move
		return;
	}

	//no piece is currently selected
	const piece = boardState[square.id];

	//only select the square if it contains a piece
	if(piece){
		//select new squre and highlight
		square.classList.add(...highLightClasses);
		selectedSquare = square;
		console.log(`Piece selected: ${piece} on ${square.id}.`);
	}else{
		selectedSquare = null; //do nothing if clicking an empty square
	}
}

//generate board once DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
	createBoard();

	//attach a single event listener to the main  board container (Event Delegation)
	const board = document.getElementById('chess-board');
	if(board){
		board.addEventListener('click', handleSquareClick);
		console.log("Click listeners attached to the board");
	}
});
