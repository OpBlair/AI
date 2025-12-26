//chess board columns
const COLUMNS: string[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

//Square colors
const lightSquare: string = 'bg-yellow-50'; //soft cream
const darkSquare: string = 'bg-amber-700'; //warm chocolate

//State and Constants for Interaction
let selectedSquare: HTMLElement | null = null;
const highLightClass = 'ring-2 ring-blue-500 ring-inset';

//Track the current Player(w for white, b for black)
let currentPlayer: 'w' | 'b' = 'w';

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

// === Utility Functions ===
interface Coords{
	col: number; // 1 to 8
	row: number; // 1 to 8
}

function getCoords(squareId: string): Coords{
	const colChar = squareId.charAt(0);
	const rowNum = parseInt(squareId.charAt(1));
	const colIndex = COLUMNS.indexOf(colChar);

	return {col: colIndex + 1, row: rowNum};
}

// === Validation for the pieces ===
//check for clear path
function isPathClear(fromId: string, toId: string, dCol: number, dRow: number): boolean{
	let current = getCoords(fromId);
	let target = getCoords(toId);

	//determine the step direction for columns and rows
	const stepCol = dCol > 0 ? 1 : dCol < 0 ? -1 : 0;
	const stepRow = dRow > 0 ? 1 : dRow < 0 ? -1 : 0;

	//move one step at a time
	current.col += stepCol;
	current.row += stepRow;

	while(current.col !== target.col || current.row !== target.row){
		const currentId = COLUMNS[current.col - 1] + current.row.toString();
		// if any square in between then path isn't clear
		if(boardState[currentId]){
			return false;
		}
		current.col += stepCol;
		current.row += stepRow;
	}
	return true;
}

//Pawn Rule
function isValidPawnMove(fromId: string, toId: string, pieceCode: string): boolean{
	const from = getCoords(fromId);
	const to = getCoords(toId);

	const isWhite = pieceCode === 'wp';
	const direction = isWhite ? 1 : -1;

	const rowDiff = (to.row - from.row) * direction;
	const colDiff = Math.abs(to.col - from.col);

	//Must move forward
	if(rowDiff <= 0 ) return false;
	if(colDiff > 1 ) return false;

	const targetPiece = boardState[toId];

	//diagonal capture 
	if(colDiff === 1){
		return rowDiff === 1 && !!targetPiece; // move forward and occupy target
	}

	//straight move
	if(targetPiece) return false; // cannot move straight into occupied square

	//one square move
	if(rowDiff === 1) return true;

	//two square move(from starting rank)
	const startRank = isWhite ? 2 : 7;
	if(from.row === startRank && rowDiff === 2){
		const middleRow = from.row + direction;
		const middleSquareId = fromId.charAt(0) + middleRow.toString();
		return !boardState[middleSquareId]; //check is  the middle square is empty
	}

	return false;
}

//Rook: Horizontal and vertical movement
function isValidRookMove(fromId: string, toId: string): boolean{
	const from = getCoords(fromId);
	const to = getCoords(toId);
	const dCol = to.col - from.col;
	const dRow = to.row - from.row;

	//strictly horizontal(dRow = 0), or vertical (dcol = 0)
	if(dCol !== 0 && dRow !== 0) return false;

	//check if path is clear
	return isPathClear(fromId, toId, dCol, dRow);
}

//Bishop: Diagonal Movement
function isValidBishopMove(fromId: string, toId: string): boolean{
	const from = getCoords(fromId);
	const to = getCoords(toId);
	const dCol = to.col - from.col;
	const dRow = to.row - from.row;

	//must move exactly diagonally(abs(dcol) == abs(dRow))
	if(Math.abs(dCol) !== Math.abs(dRow) || dCol === 0) return false;

	//check if path is clear
	return isPathClear(fromId, toId, dCol, dRow);
}

//Queen: Horizontal, Vertical, diagonal, movement
function isValidQueenMove(fromId: string, toId: string): boolean{
	return isValidRookMove(fromId, toId) || isValidBishopMove(fromId, toId);
}

//Knight: L-shape movement (2 squares in one direction, 1 square perpendicular)
function isValidKnightMove(fromId: string, toId: string): boolean{
	const from = getCoords(fromId);
	const to = getCoords(toId);
	const dCol = Math.abs(to.col - from.col);
	const dRow = Math.abs(to.row - from.row);

	//Must be (2,1) or (1,2) in difference
	return (dCol === 2 && dRow === 1) || (dCol === 1 && dRow === 2);
}

//King: one square in any direction * castling logic is handled in backend *
function isValidKingMove(fromId: string, toId: string): boolean{
	const from = getCoords(fromId);
	const to = getCoords(toId);
	const dCol = Math.abs(to.col - from.col);
	const dRow = Math.abs(to.row - from.row);

	//Must move exactyl 1 square away
	return dCol <= 1 && dRow <= 1 && (dCol !== 0 || dRow !== 0);
}

// === Master Validation ===
function isValidMove(fromId: string, toId: string, pieceCode: string): boolean{
	const targetPiece = boardState[toId];

	//1. get color of the piece being moved
	const movingColor = pieceCode.charAt(0);

	//2. Rule: cannot capture your own piece
	if(targetPiece && targetPiece.charAt(0) === movingColor){
		console.log("Validation Failed: Cannot Capture own piece.");
		return false;
	}

	//3. Rule: Check Piece-Specific Rules
	const pieceType = pieceCode.charAt(1);

	switch(pieceType){
		case 'p' : return isValidPawnMove(fromId, toId, pieceCode);
		case 'r' : return isValidRookMove(fromId, toId);
		case 'b' : return isValidBishopMove(fromId, toId);
		case 'q' : return isValidQueenMove(fromId, toId);
		case 'n' : return isValidKnightMove(fromId, toId);
		case 'k' : return isValidKingMove(fromId, toId);
		default : return false;
	}
}

// === RENDERING AND BOARD CREATION ===

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

// === EVENT HANDLING ===

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

		//Move piece Logic
		const fromSquareId = selectedSquare.id;
		const toSquareId = square.id;
		const pieceCode = boardState[fromSquareId];

		if(pieceCode){
			// === Validation Check ===
			if(!isValidMove(fromSquareId, toSquareId, pieceCode)){
				// if the move is illegal, deselect the piece and exit
				selectedSquare = null;
				console.log(`Illegal move attempted: ${pieceCode} from ${fromSquareId} to ${toSquareId}`);
				return;
			}
			// --- Execute the Move ---
			boardState[toSquareId] = pieceCode;
			boardState[fromSquareId] = null;

			//update the DOM
			renderPiece(square, pieceCode);
			renderPiece(selectedSquare, null);
			console.log(`Moved ${pieceCode} from ${fromSquareId} to ${toSquareId}`);

			sendDataToBackend(fromSquareId, toSquareId);

			//Switch the turn
			currentPlayer = currentPlayer === 'w' ? 'b' : 'w';
			updateTurnIndicator();
			console.log(`Turn switched to : ${currentPlayer === 'w' ? 'White' : 'Black'}`);
		}

		selectedSquare = null; //clear selection after move
		return;
	}

	//no piece is currently selected
	const piece = boardState[square.id];

	//only select the square if it contains a piece
	if(piece){
		//Only select pieces of the current player's color
		const pieceColor = piece.charAt(0);
		if(pieceColor !== currentPlayer){
			console.log(`Selection Failed: It's ${currentPlayer === 'w' ? 'White' : 'Black'}'s turn.`);
			selectedSquare = null;
			return;
		}

		//select new squre and highlight
		square.classList.add(...highLightClasses);
		selectedSquare = square;
		console.log(`Piece selected: ${piece} on ${square.id}.`);
	}else{
		selectedSquare = null; //do nothing if clicking an empty square
	}
}

//Turn indicator
function updateTurnIndicator(): void{
	const indicator = document.getElementById('turn-indicator');
	const container = document.getElementById('turn-indicator-container');
	if(indicator && container){
		const isWhite = currentPlayer === 'w';
		const color = currentPlayer === 'w' ? 'White' : 'Black';

		//update text color
		indicator.classList.remove('text-stone-900', 'text-gray-200');
		const textColor = isWhite ? 'text-stone-900' : 'text-gray-200';
        indicator.classList.add(textColor);

        //update container background
        container.classList.remove('bg-yellow-50', 'bg-amber-700');
        const bgColor = isWhite ? 'bg-yellow-50' : 'bg-amber-700';
        container.classList.add(bgColor);

        //update the text content
		indicator.textContent = `${color} to Move`;
	}
}

// === AI move update to the UI
function applyAIMove(aiMove: {from_square: string, to_square: string, piece_code: string, message?:string}){
	const {from_square, to_square, piece_code} = aiMove;

	//update the board state
	boardState[to_square] = piece_code;
	boardState[from_square] = null;

	//update the DOM
	const fromCell = document.getElementById(from_square);
	const toCell = document.getElementById(to_square);

	if(fromCell && toCell){
		renderPiece(toCell, piece_code);
		renderPiece(fromCell, null);
	}

	console.log(aiMove.message || `AI moved ${piece_code} from ${from_square}`);
}

// === API Communication Function ===
async function sendDataToBackend(fromId: string, toId: string): Promise<void> {
	const dataToSend = {
		boardState: boardState,
		currentPlayer: currentPlayer,
		lastMove: {from: fromId, to: toId}
	};

	console.log("Sending move to backend for testing...");

	// Simulate giving the AI a moment to "THINK" (1 second delay).
	setTimeout(async () => {
			try{
			const response = await fetch('http://127.0.0.1:5000/api/ai_move', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(dataToSend),
			});

			if(!response.ok){
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const result = await response.json();
			console.log("Backend Response:", result);

			updateCheckVisuals(result.isWhiteInCheck, 'w');
			updateCheckVisuals(result.isBlackInCheck, 'b');

			if(result.status === 'move_found'){
				applyAIMove(result);
				currentPlayer = 'w';
				updateTurnIndicator();
			}
		} catch(error){
			console.error('Failed to communicate with the backend:', error);
		}
	}, 1000);
}

// === Identify the King ===
function findKingSquare(color: 'w' | 'b'): string | null {
	for(const [square, piece] of Object.entries(boardState)){
		if(piece == color + 'k') return square;
	}
	return null;
}

// === Visual Feedback ===
function updateCheckVisuals(isCheck: boolean = false, color: 'w' | 'b'){
	const kingSq = findKingSquare(color);
	if(!kingSq) return;

	const kingElement = document.getElementById(kingSq);
	if(kingElement){
		if(isCheck){
		kingElement.classList.add('ring-4', 'ring-red-500', 'shadow-[0_0_20px_rgba(239,68,68,0.8)]', 'animate-pulse');
		}else{
			kingElement.classList.remove('ring-4', 'ring-red-500', 'shadow-[0_0_20px_rgba(239,68,68,0.8)]', 'animate-pulse');
		}
	}
}

//generate board once DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
	createBoard();
	updateTurnIndicator();
	//attach a single event listener to the main  board container (Event Delegation)
	const board = document.getElementById('chess-board');
	if(board){
		board.addEventListener('click', handleSquareClick);
		console.log("Click listeners attached to the board");
	}
});

