class Filters():
    def __init__(self):
        self.practice_tests = ["Ptest #1 (202003U)","Ptest #2 (202012A)","Ptest #3 (202010A)",
                    "Ptest #4 (202011U)","Ptest #5 (202012U)","Ptest #6 (202009U)",
                    "Ptest #7 (202010SD)","Ptest #8 (202010U)","Ptest #9 (202103A)","Ptest #10 (202103U)",
                    "Ptest #11 (201912U)","Ptest #12 (202009A)","Ptest #13 (202008A)","Ptest #14 (201911U)",
                    "Ptest #15 (202105U)","Ptest #16 (201905U)","Ptest #17 (201910U)","Ptest #18 (201905A)",
                    "Ptest #19 (201903U)","Ptest #20 (202105A)","Ptest #21 (202306U)","Ptest #22 (202304SD)",
                      "Ptest #23 (202305U)","D Practice Test #1", "D Practice Test #2", "D Practice Test #3","D Practice Test #4",

                      "NL Practice Test #1","NL Practice Test #2","NL Practice Test #3","NL Practice Test #4"]
        self.category = ["HOA","PSDA","PAM","GEOM","Vocab","Big Picture","Reading for Function","Literal Comprehension","Text Completion","Supporting Evidence", "Graphs and Charts","Comma Uses and Misuses","Subject-verb agreement","Combining and Separating Sentences","Essential and Non-essential clauses","Transitions","Plain Text"]
        self.sub_category_one = ['Linear Functions Part 1','Angles and Triangles','Intro to Functions','Linear Functions Part 2','Polynomial Expressions','Rational Expressions','Special Cases','Right Triangles & Trig','Exponential Functions','Quadratic Equations',
        'Isolating Variables',
        'Systems of Equations',
        'Linear Equations',
        'Interpreting Graph',
        'Two-Way Tables',
        'Scatter Plots',
        'Percents',
        'Unit Conversions',
        'Data and Stats 1',
        'Rates',
        'Rational Functions',
        'Quadratic & Polynomial Functions',
        'Linear vs. Exponential Functions',
        'Ratios',
        'Planar Geometry',
        'Solid Geometry',
        'Equation of a Circle',
        'Exponential Equations',
        'Absolute Value',
        'Probability',
        'Radical Equations',
        'Similar Triangles',
        'Linear Equations and Inequalities WP',
        'Parallel and Perpendicular Lines',
        'Circle Ratios',
        'Exponential & Radical Expressions',
        'Rational Equations',
        'Complex Numbers',
        'Data and Stats 2']
        self.sub_category_two =[
            "Deriving Equation", "Parallel Lines & Transversals", "Evaluating", "Deriving Inequality", "Adding/Subtracting",
            "POG", "Dividing", "Linear Equations", "Pythagorean", "Finding y-int", "SOS",
            "NA", "Finding Slope", "Substitution", "Factoring", "Fractions & Decimals", "45-45-90",
            "Line Graph", "Fraction of", "Predicted Value", "Percent of", "Single Conversion", "Median",
            "Interpreting", "Deriving Graph", "30-60-90", "Mixed", "Word Problem", "Factored Form",
            "Unit Circle", "Probability", "Number of Solutions", "Special Cases", "Elimination", "Direct Proportionality",
            "Finding Area", "Greater/Less than", "Intercepts", "Finding Volume", "Adding & Subtracting", "Quadratic Formula",
            "Shift", "Base Reduction", "Distributing", "Finding Perimeter", "Solving", "Mean",
            "Data Set", "Basic", "Range", "Multiplying", "Comparing", "Standard Form",
            "Congruency", "Create & Solve", "Systems of Equations", "sinx=cosy", "Interpreting Equation", "Percent Inc/Dec",
            "Cubic", "Proportions", "OG", "Finding Arc Length", "Interpreting Graph", "Vertex Form",
            "Inequality Graph", "Isosceles", "Product Rule", "Linear Combination", "Trig", "Actual vs. Predicted",
            "Percent Change", "Sub & Solve", "Pie Chart", "Population Density", "Finding Length", "Tangent Line",
            "Standard Deviation", "Rate to Rate", "Classic", "Proof", "Easy", "General Form",
            "Radical to Exponential", "Sum of Solutions", "Finding Solution", "Outlier", "Skew", "Definition",
            "Reverse", "Square Root Method", "Graph", "Cylinder", "Linear Function", "Quadratic Function",
            "Finding Surface Area", "Finding x-int", "Constants", "Rectangular Prism", "Create & Sub", "Triple",
            "Hard", "Finding Area of Shaded Region", "Triangles", "Average Speed", "Inequality", "Finding Ratio",
            "Fractions", "Long Division", "PTSI", "Double Conversion", "How many times", "Bar Graph",
            "Finding Radius", "Reading Graph", "Arc Length and Angle", "Equation", "Extraneous Solutions", "Area",
            "Vertical Angles", "Angle sum of Quadrilaterals", "Zeros from equation", "Quotient Rule", "Directly Proportional", "Margin of Error",
            "Sample Selection", "Likelihood", "Proving", "Finding Width", "Degrees and Radians", "Create Equation & Solve",
            "Right Triangle", "Percent Mixed", "Finding Value", "Solving for x", "Volume", "Parallel",
            "Single", "Finding Intercepts", "Deriving Table", "Ratio", "Finding intercepts", "Perpendicular",
            "Finding Arc Measure", "Proportion", "Max", "y-int", "Radians & Degrees", "Pythagorean Theorem",
            "Multi-Dimensional", "Radical as well", "Finding Predicted y-value", "Perimeter", "Complex", "Surface Area",
            "Radical to Exponential ", "x-int", "Density", "POS", "Deriving Expression", "Min", "Comparing Means", "Finding Angle", "Square root method"
        ]
        self.sub_category_three = [
            "Table", "Finding Angle", "f(a)", "NA", "Slope-Intercept Form", "Table to Graph", "Perfect Square", "Points", "Infinitely Many Solutions", "Trapezoid", "Equation", "Factoring", "Word Problem", "Graph", "Factored Form", "Square", "Part", "Box-Plot", "Whole", "Frequency Table", "Standard Form", "Inequality", "Triangle + Kite", "Bar Graph", "Finding vertex", "Scatter Plots", "Constants", "Unit Circle", "Elimination", "Discriminant", "Finding x-int", "No Solution", "Data Set", "Parallelogram", "Diameter", "Right Triangle", "Decimals", "Asymptote", "Ratio & Area", "Trick", "Deriving Graph", "Trig", "Perpendicular", "One-Variable", "New", "Percent Inc/Dec", "Dot Plot", "Percent", "Function Notation", "Deriving Equation", "One Solution", "Proving", "Geometric Mean", "Decrease", "Quadratic Equation", "Finding Radius", "Rectangle", "Frequency", "Substitution", "Line Graph", "If", "A>1", "Rate to Rate", "Interpreting", "Finding Sine and Cosine", "How Many Times", "Increase", "Finding Sine", "Distributing negative", "Unit Conversion", "Finding Ratio", "Product Rule", "Ratio", "Finding Center", "A=1", "f(0)", "Extraneous Solutions", "y-int", "Interpreting intercept", "Cylinder", "Finding Cosine", "Square Root Method", "Quadratic Formula", "Outer-Inner", "Hour Glass", "Finding Sine and Tangent", "Difference of Squares", "Finding Circumference", "Mixed", "y", "Finding Solution", "Vertex Form", "Area", "Finding Sum of x-coordinates", "Radical to Exponential", "Initial Amount", "Rationalizing", "Radius and Angle", "U-Sub", "y-value", "Triangle", "f(x)=a", "Solving", "Scale", "Circle", "Finding Side Length", "PTSI", "Distributing Negative", "Finding y-value", "Sphere", "f(x)=0", "Finding Perimeter", "x", "Rate of Change", "Proof", "X^4", "Triangle and Circle", "Reading Graph", "Equations", "Cube", "Standard to General Form", "Cylinder and Sphere", "Equation and Point", "Dividing", "Shift", "Grouping", "Absolute Value", "Adding & Subtracting", "Rectangle and Semi-Circle", "Finding Max", "Form", "Radius", "Diff of Squares", "PFT", "Constants", "GCF", "Slope and Point", "Right Triangles", "Deriving", "Rectangular Prism", "Sub and Solve", "Definition", "Cone", "Finding Area", "a=1", "Linear", "Cosine", "Finding Vertex", "Sub & Solve", "Word Problems", "One-Step", "x=a", "From Equation", "Tangent", "Infinitely Many", "Both", "Isosceles Right Triangle", "Similarity", "a>1", "Function", "Sine", "Time", "Finding Slope", "Exponential Function", "Radians to degrees", "x-int", "POG", "Angle", "Squared", "Two-Step", "Exponential", "Factored", "From Graph", "Inscribed Square", "Histogram", "Rate Word Problem", "How many times", "Quadratic Function", "Single", "Percent of", "Combined Mean", "Finding x", "Max", "Radians to Degrees", "Find height", "Directly Proportional", "Finding y", "Initial", "Outer - Inner", "Finding Diameter", "Rate word problem", "System of Inequality", "Classic", "Deriving Table", "Double Bubble", "Factor by grouping", "Multi-step", "Exponential Functions", "Isosceles Triangle", "Solving for y", "Finding Constants", "Percent greater"
        ]
        self.difficulty = ["1","2","3","4","5"]
        self.correctness = {
                "Correct":"1",
                "Incorrect":"0"
                }
        self.section = ["1","2","2E","2H","3","4"]
            

    
