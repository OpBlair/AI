// Define the columns for board coordinates
const COLUMNS: string[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

/**
 * Generates the 8x8 chess board structure dynamically.
 * npm install typescript --save-dev
 * npx tsc --init
 * 
 * tsconfig.json
 * {
  "compilerOptions": {
    "target": "ES2020",          Compile to modern JavaScript 
    "module": "CommonJS",       How modules are handled
    "outDir": "./",              Output compiled files to the same directory 
    "rootDir": "./",             Look for source files in the same directory 
    "strict": true,              Enable all strict type-checking options (recommended) 
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
npx tsc
 */
function createBoard(): void {
    // We use a type assertion here because we know 'chess-board' exists in the HTML
    const board = document.getElementById('chess-board') as HTMLElement;
    // Inside your createBoard function in board.ts:

    // ...

    // Clear any existing content (good for a 'reset' function later)
    board.innerHTML = ''; 

    // Loop through the rows (from 8 down to 1)
    for (let row: number = 8; row >= 1; row--) {
        // Loop through the columns (from 'a' to 'h')
        for (let colIndex: number = 0; colIndex < 8; colIndex++) {
            const col: string = COLUMNS[colIndex];
            
            // Standard chess rule: a8 is a dark square.
            // (row + colIndex) is even for dark squares (8+0=8, 7+1=8, 6+0=6, etc.)
            const isDarkSquare: boolean = (row + colIndex) % 2 === 0;
            
            // Assign Tailwind classes for the two colors
            const bgColor: string = isDarkSquare ? 'bg-gray-500' : 'bg-amber-100';
            
            // Create the square element
            const square: HTMLDivElement = document.createElement('div');
            
            // Assign a unique ID (e.g., "a8", "h1")
            square.id = `${col}${row}`; 
            
            // Use data attributes for easy programmatic access to coordinates
            square.dataset.row = row.toString();
            square.dataset.col = col;

            // Apply Tailwind classes for size and color/flex alignment
            square.className = `
                w-12 h-12 md:w-16 md:h-16 
                flex items-center justify-center 
                ${bgColor} 
                transition duration-100 ease-in-out
            `;
            
            board.appendChild(square);
        }
    }
    
    console.log("TypeScript: Empty chess board structure created.");
}

// Ensure the board generation runs once the HTML document is fully loaded
document.addEventListener('DOMContentLoaded', createBoard);


// Define the columns for board coordinates
const COLUMNS: string[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

// --- Define the Colors ---
// Recommended Classic Wood Scheme for best contrast
const LIGHT_SQUARE_COLOR: string = 'bg-yellow-100'; // Light, creamy color
const DARK_SQUARE_COLOR: string = 'bg-amber-800';  // Deep, rich brown/gold

/**
 * Generates the 8x8 chess board structure dynamically.
 */
function createBoard(): void {
    // We use a type assertion here because we know 'chess-board' exists in the HTML
    const board = document.getElementById('chess-board') as HTMLElement;
    
    // Clear any existing content
    board.innerHTML = ''; 

    // Loop through the rows (from 8 down to 1)
    for (let row: number = 8; row >= 1; row--) {
        // Loop through the columns (from 'a' to 'h')
        for (let colIndex: number = 0; colIndex < 8; colIndex++) {
            const col: string = COLUMNS[colIndex];
            
            // Standard chess rule: a8 is a dark square.
            // (row + colIndex) is even for dark squares (8+0=8, 7+1=8, etc.)
            const isDarkSquare: boolean = (row + colIndex) % 2 === 0;
            
            // --- UPDATED COLOR ASSIGNMENT ---
            // Use the constants defined above for the board colors
            const bgColor: string = isDarkSquare ? DARK_SQUARE_COLOR : LIGHT_SQUARE_COLOR;
            
            // Create the square element
            const square: HTMLDivElement = document.createElement('div');
            
            // Assign a unique ID (e.g., "a8", "h1")
            square.id = `${col}${row}`; 
            
            // Use data attributes for easy programmatic access to coordinates
            square.dataset.row = row.toString();
            square.dataset.col = col;

            // Apply Tailwind classes for size and color/flex alignment
            square.className = `
                w-12 h-12 md:w-16 md:h-16 
                flex items-center justify-center 
                ${bgColor} 
                transition duration-100 ease-in-out
            `;
            
            board.appendChild(square);
        }
    }
    
    console.log("TypeScript: Chess board created with Classic Wood colors.");
}

// Ensure the board generation runs once the HTML document is fully loaded
document.addEventListener('DOMContentLoaded', createBoard);