// prompt 1: create a basic uart verilog BFM
// prompt 2: I want it in pure verilog

`timescale 1ns/1ps

module uart_bfm;

    // UART lines
    reg tx;
    reg rx;

    // Parameters
    parameter BAUD_RATE = 230400;
    real bit_time;

    initial begin
        bit_time = 1e9 / BAUD_RATE; // bit time in ns
        tx = 1'b1; // idle state
    end

    // ----------------------------------------
    // TASK: Send one byte (LSB first)
    // ----------------------------------------
    task uart_send_byte;
        input [7:0] data;
        integer i;
        begin
            // Start bit
            tx = 1'b0;
            #(bit_time);

            // Data bits
            for (i = 0; i < 8; i = i + 1) begin
                tx = data[i];
                #(bit_time);
            end

            // Stop bit
            tx = 1'b1;
            #(bit_time);
        end
    endtask

    // ----------------------------------------
    // TASK: Receive one byte
    // ----------------------------------------
    task uart_recv_byte;
        output [7:0] data;
        integer i;
        begin
            data = 8'b0;

            // Wait for start bit
            wait (rx == 1'b0);

            // Move to middle of first data bit
            #(bit_time + bit_time/2);

            // Sample 8 bits
            for (i = 0; i < 8; i = i + 1) begin
                data[i] = rx;
                #(bit_time);
            end

            // Wait for stop bit (optional)
            #(bit_time);
        end
    endtask

endmodule
