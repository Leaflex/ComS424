#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def myGaussianElim(A, B):
    n = len(B)

    for i in range(n):
        # Partial pivoting: swap rows if needed
        max_row = i + np.argmax(np.abs(A[i:, i]))
        if i != max_row:
            A[[i, max_row]] = A[[max_row, i]]  # Swap rows in A
            B[i], B[max_row] = B[max_row], B[i]  # Swap corresponding B values
        
        # Set diagonals to 1
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] = A[i][j] / factor
        B[i] = B[i] / factor

        # Eliminate lower triangle
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            B[k] -= factor * B[i]

    # Back substitution
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = B[i]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]

    return x

def plot_results(x_values, y_values, coeffs):
    # Define the polynomial function p(x) from the coefficients
    def polynomial(x):
        return coeffs[0]*x**3 + coeffs[1]*x**2 + coeffs[2]*x + coeffs[3]

    # Create an array of x-values for plotting the polynomial
    print(x_values)
    x_poly = np.linspace(min(x_values), max(x_values), 500)
    y_poly = polynomial(x_poly)

    # Plot the original points (x_values, y_values)
    plt.scatter(x_values, y_values, color='red', label='Original Points f(x)')

    # Plot the polynomial curve p(x)
    plt.plot(x_poly, y_poly, color='blue', label='Polynomial p(x)')

    # Add title, legend, and labels
    plt.title('Original Points vs. Polynomial Fit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

def p_4(filename):
    '''
    Creates numpy array for 4th degree linear system from input file of points.
    
    A = np.array([
        [-0.001, 0.01, -0.1, 1.0],
        [-0.000008, 0.0004, -0.02, 1.0],
        [0.000008, 0.0004, 0.02, 1.0],
        [0.001, 0.01, 0.1, 1.0],
    ], dtype=float)
    
    B = np.array([0.9950041653, 0.9998000067, 0.9998000067, 0.9950041653], dtype=float)
    '''
    
    fid = open(filename, 'r')

    A = np.array([]).reshape(0, 4)  # Prepare A as a 2D array (equation system)
    B = np.array([])  # B as a 1D array for constants

    while True:
        line = fid.readline()
        if not line:
            break

        # Split the line to get the point values
        point = line.split(', ')
        x_value_str = point[0].strip()

        # Replace any Unicode minus signs with regular minus signs
        x_value_str = x_value_str.replace('−', '-')  # Fix Unicode minus
        x_value = float(x_value_str)

        # Create the equation coefficients from x_value
        equation = np.array([x_value**3, x_value**2, x_value, 1])

        # Append to matrix A
        A = np.vstack([A, equation])

        # Extract the y-value (either cos, sin, tan, or just a number)
        b_value = point[1].strip()
        if 'cos' in b_value:
            b_value = np.cos(float(b_value.strip('cos()\n').replace('−', '-')))
        elif 'sin' in b_value:
            b_value = np.sin(float(b_value.strip('sin()\n').replace('−', '-')))
        elif 'tan' in b_value:
            b_value = np.tan(float(b_value.strip('tan()\n').replace('−', '-')))
        else:
            b_value = float(b_value.replace('−', '-').strip())

        # Append to vector B
        B = np.append(B, b_value)

    fid.close()
    return (A, B)

def main():
    A, B = p_4('inputs/input.txt')
    a = A.copy()
    b = B.copy()

    print(f'A: {A}')
    print(f'B: {B}\n')

    numpyOutput = np.linalg.solve(A.copy(), B.copy())
    print(f"np.linalg.solve(A, B): {numpyOutput}\n")

    myOutput = [float(x) for x in myGaussianElim(A, B)]
    print(f"myGaussianElim(A, B): {myOutput}\n")

    # Check if the results are close within the tolerance
    comparison = np.allclose(myOutput, numpyOutput, atol=1e-12)
    print(f"Are the results within tolerance (1e-12)? {comparison}")

    # Plot the results
    plot_results([-0.1, -0.02, 0.02, 0.1], b, myOutput)

if __name__ == '__main__':
    main()
