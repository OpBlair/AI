document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('chess-board');
    
    // Define the column labels for easy coordinate assignment
    const columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

    // Loop through the rows (from 8 down to 1)
    for (let row = 8; row >= 1; row--) {
        // Loop through the columns (from 'a' to 'h')
        for (let colIndex = 0; colIndex < 8; colIndex++) {
            const col = columns[colIndex];
            
            // Calculate the total index to determine the color.
            // (row + colIndex) is odd for dark squares starting from a8 (8+0=8, 8%2=0 - wait, depends on how you define dark/light)
            // Let's ensure a8 (row 8, col index 0) is a dark square as per standard chess colors.
            // 8 + 0 = 8 (Even number) -> Let's map even to the "dark" color (bg-gray-500)
            const isDarkSquare = (row + colIndex) % 2 === 0;
            
            // Assign Tailwind classes for color
            const bgColor = isDarkSquare ? 'bg-gray-500' : 'bg-amber-100';
            
            // Create the square element
            const square = document.createElement('div');
            
            // Assign a unique ID (e.g., "8a", "1h")
            square.id = `${col}${row}`; 
            
            // Use data attributes to store the coordinates
            square.dataset.row = row;
            square.dataset.col = col;

            // Apply Tailwind classes for size and color
            square.className = `
                w-12 h-12 md:w-16 md:h-16 
                flex items-center justify-center 
                ${bgColor}
            `;
            
            // Append the square to the board container
            board.appendChild(square);
        }
    }
    
    console.log("Empty chess board generated successfully!");
});