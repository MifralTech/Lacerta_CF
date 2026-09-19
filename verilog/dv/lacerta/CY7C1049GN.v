module CY7C1049GN (
    input  wire [15:0] A,     // Address (512K locations)
    inout  wire [7:0]  DQ,    // Data bus
    input  wire        CE_n,  // Chip Enable (active low)
    input  wire        OE_n,  // Output Enable (active low)
    input  wire        WE_n   // Write Enable (active low)
);

    // Memory array: 512K x 8
    //reg [7:0] mem [0:524287]; // Manually changed this to below, as we are using only 16 bits for lacerta
    reg [7:0] mem [0:(2**16)-1];

    // Internal data register for output
    reg [7:0] data_out;

    // Tri-state control
    assign DQ = (!CE_n && !OE_n && WE_n) ? data_out : 8'bz;

    // Write operation
    always @(*) begin
        if (!CE_n && !WE_n) begin
            mem[A] = DQ;
        end
    end

    // Read operation
    always @(*) begin
        if (!CE_n && WE_n) begin
            data_out = mem[A];
        end
    end

endmodule
