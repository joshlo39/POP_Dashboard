class Filters():
    def __init__(self):
        self.practice_tests = ["Ptest #1 (202003U)","Ptest #2 (202012A)","Ptest #3 (202010A)",
                    "Ptest #4 (202011U)","Ptest #5 (202012U)","Ptest #6 (202009U)",
                    "Ptest #7 (202010SD)","Ptest #8 (202010U)","Ptest #9 (202103A)","Ptest #10 (202103U)",
                    "Ptest #11 (201912U)","Ptest #12 (202009A)","Ptest #13 (202008A)","Ptest #14 (201911U)",
                    "Ptest #15 (202105U)","Ptest #16 (201905U)","Ptest #17 (201910U)","Ptest #18 (201905A)",
                    "Ptest #19 (201903U)","Ptest #20 (202105A)","Ptest #21 (202306U)","Ptest #22 (202304SD)",
                    "Ptest #23 (202305U)","D Practice Test #1", "D Practice Test #2", "D Practice Test #3","D Practice Test #4",
                    "D Practice Test #5","D Practice Test #6","CBQB","NL Practice Test #1","NL Practice Test #2","NL Practice Test #3"
                    ,"NL Practice Test #4","NL Practice Test #5","NL Practice Test #6","June 2023 I"]
        self.category = ["HOA","PSDA","PAM","GEOM","Vocab","Big Picture","Reading for Function","Literal Comprehension","Text Completion","Supporting Evidence", "Graphs and Charts","Comma Uses and Misuses","Subject-verb agreement","Combining and Separating Sentences","Essential and Non-essential clauses","Transitions","Plain Text","Notes","Paired Text","Parts of Speech","Plural v. Possessive","Pronoun/Noun Agreement","Punctuation","Reading for Function","Subject-verb agreement","Supporting Evidence","Text Completion","Text Structure","Transitions","Use of preposition"]

        self.sub_category_one = ['Absolute Value','Angles and Triangles','Circle Ratios','Complex Numbers','Data and Stats 1','Data and Stats 2','Equation of a Circle','Exponential & Radical Expressions','Exponential Equations','Exponential Functions','Interpreting Graph','Intro to Functions','Isolating Variables','Linear Equations','Linear Equations and Inequalities WP','Linear Functions Part 1','Linear Functions Part 2','Linear vs. Exponential Functions','NA','Parallel and Perpendicular Lines','Percents','Planar Geometry','Polynomial Expressions','Probability','Quadratic & Polynomial Functions','Quadratic Equations','Radical Equations','Rates','Rational Equations','Rational Expressions','Rational Functions','Ratios','Right Triangles & Trig','Scatter Plots','Similar Triangles','Solid Geometry','Special Cases','Systems of Equations','Two-Way Tables','Unit Conversions',"Author's Purpose","Colon","Colon-Usage","Comma Usage","Comma Uses","Comma Uses and Misuses","Conjunction","Dashes","Drawing Conclusions","Essential and Non-Essential Clauses","Essential and Non-essential Clauses","Essential and Nonessential Clauses","Graphic Analysis","History","Illustrate Claim","Illustrate a Claim","Illustrating","Independent-Dependent Clauses","Inference-Drawing Conclusion","Infographic","Literal Comprehension","Literary Fiction","Main Idea","Main Purpose","Modifier","Modifiers","Parallel Structure","Parts of Speech","Poetry","Pronoun Usage","Pronoun/Noun Agreement","Prounouns and Contractions","Punctuation","RFF","RFF/LC","Reading for Function","Refute a Claim","Refuting","Science","Semi-Colon","Semi-Colon Usage","Sentence Clarity?","Social Science","Subject-Verb Agreement","Supoorting Detail","Support Claim","Support the Claim","Supporting","Supporting Detail","Supporting Evidence","Supporting a Claim","Tense","Text Completion","Transitions","Use of Preposition","Verb Tense","Weaken Claim","Word Choice and Diction","colon and semi-colon","colon usage","conjunction","conjunction usue","dash","essential v nonessential","Non-essential Clauses","poetry","prepositions","pronoun","pronoun usage","punctuation","semi colon","semi colon and colon usage","semi colons","semi-colon usage","structure of text","subject verb agreement","supporting a claim","supporting evidence","supporting/ contradicting a claim","text completion","transitions","verb gerund","verb tense"]
        self.sub_category_two = ['30-60-90','45-45-90','Actual vs. Predicted','Adding & Subtracting','Adding/Subtracting','Algebraic Expression','Angle sum of Quadrilaterals','Arc Length and Angle','Area','Average Rate of Change','Average Speed','Bar Graph','Base Reduction','Basic','Circles','Circumference','Classic','Comparing','Comparing Means','Complex','Congruency','Constants','Create & Solve','Create & Sub','Create Equation & Solve','Cubic','Cylinder','Data Set','Definition','Degrees and Radians','Density','Deriving','Deriving Equation','Deriving Expression','Deriving Graph','Deriving Inequality','Deriving Table','Direct Proportionality','Directly Proportional','Distributing','Dividing','Double','Double Conversion','Easy','Elimination','Equation','Evaluating','Evaluating Functions','Extraneous Solutions','Factored Form','Factoring','Finding Angle','Finding Arc Length','Finding Arc Measure','Finding Area','Finding Area of Shaded Region','Finding Intercepts','Finding Length','Finding Perimeter','Finding Predicted y-value','Finding Radius','Finding Rate','Finding Ratio','Finding Slope','Finding Solution','Finding Surface Area','Finding Volume','Finding Width','Finding x-int','Finding y-int','Fraction of','Fractions','Fractions & Decimals','General Form','Graph','Greater/Less than','Hard','How many times','Inequality','Inequality Graph','Inference','Intepreting Equation','Intercepts','Interpreting','Interpreting Equation','Interpreting Functions','Interpreting Graph','Interpreting Point','Isosceles','Likelihood','Line Graph','Linear Combination','Linear Equations','Linear Function','Long Division','MIxed','Margin of Error','Max','Mean','Median','Min','Mixed','Multi-Dimensional','Multiplying','NA','Number of Solutions','OG','Outer-Inner','Outlier','POG','POS','PTSI','Parallel','Parallel Lines & Transversals','Parallel Lines and Transversals','Percent','Percent Change','Percent Inc/Dec','Percent Increase','Percent Mixed','Percent of','Perimeter','Perpendicular','Pie Chart','Point','Population Density','Population Estimate','Predicted Value','Probability','Product Rule','Proof','Proportion','Proportions','Proving','Pythagorean','Pythagorean Theorem','Quadratic Formula','Quadratic Function','Quotient Rule','Radians & Degrees','Radical as well','Radical to Exponential','Range','Rate of Change','Rate to Rate','Ratio','Reading Graph','Rectangular Prism','Reverse','Right Triangle','SOS','Sample Selection','Scale Factor','Shift','Single','Single Conversion','Skew','Solving','Solving for x','Special Cases','Square Root Method','Square root method','Standard Deviation','Standard Form','Standard Form Graph','Sub & Solve','Substitution','Sum of Solutions','Surface Area','Systems of Equations','Tangent Line','Triangles','Trick','Trig','Triple','Unit Circle','Vertex Form','Vertical Angles','Volume','Word Problem','Word Problems','Zeros from equation','crazy shit','sinx=cosy','x-int','y-int'"Comma","Comma Usage","Comma Uses and Misuses","Commonly confused word pairs","Double","Essential and Non-essential Clauses","Essential-Nonessential Clauses","Fiction","Graphic Analysis","History","Idiom","Illustrate Claim","Independent-Dependent Clauses","Literary Fiction","Parts of Speech","Poetry","Punctuation","Science","Semicolon","Semicolons","Sentence Structure","Short-Story","Social Science","Subject-Verb Agreement","Text Completion","comma usage","fanboy","plural v possesive","poetry","semi-colon use","text completion"]

        self.sub_category_three = ['A=1','A>1','Absolute Value','Adding & Subtracing','Angle','Area','Asymptote','Bar Graph','Basic','Bias','Both','Box-Plot','Circle','Classic','Combined Mean','Cone','Constants','Conversion','Cosine','Create & Solve','Create and Solve','Cube','Cube & Cylinder','Cup','Cylinder','Cylinder and Sphere','Data Conclusion','Data Set','Decay Factor','Decimals','Decrease','Definition','Deriving','Deriving Equation','Deriving Graph','Deriving Table','Diameter','Diff of Squares, PFT, Constants','Difference of Squares','Directly Proportional','Discriminant','Distributing','Distributing Negative','Distributing negative','Dividing','Dot Plot','Double Bubble','Double-Bubble','Elimination','Equation','Equation and Point','Equations','Exponential','Exponential Function','Exponential Functions','Extraneous Solutions','Factor by grouping','Factored','Factored Form','Factoring','Find height','Finding Angle','Finding Area','Finding Center','Finding Circumference','Finding Constants','Finding Cosine','Finding Diameter','Finding Max','Finding Perimeter','Finding Radius','Finding Ratio','Finding Side Length','Finding Sine','Finding Sine and Cosine','Finding Sine and Tangent','Finding Slope','Finding Solution','Finding Sum of x-coordinates','Finding Vertex','Finding vertex','Finding x','Finding x-int','Finding y','Finding y-value','Form','Fractions & Decimals','Frequency','Frequency Table','From Equation','From Graph','Function','Function Notation','GCF','Generalization','Geometric Mean','Given Center and Radius','Graph','Grouping','Histogram','Hour Glass','How Many Times','How many times','If','Increase','Inequality','Infinitely Many','Infinitely Many Solutions','Initial','Initial Amount','Inscribed Square','Interior of Circle','Interpreting','Interpreting intercept','Isosceles Right Triangle','Isosceles Triangle','Line Graph','Linear','Max','Mixed','Multi-step','NA','New','No Solution','No Solutions','One Solution','One-Step','One-Variable','Outer - Inner','Outer-Inner','POG','PST','PTSI','Parallelogram','Part','Percent','Percent Inc/Dec','Percent greater','Percent of','Perfect Square','Perpendicular','Points','Product Rule','Proof','Proving','Quadratic Equation','Quadratic Formula','Quadratic Function','Radians to Degrees','Radians to degrees','Radical to Exponential','Radius','Radius and Angle','Rate Word Problem','Rate of Change','Rate to Rate','Rate word problem','Ratio','Ratio & Area','Rationalizing','Reading Graph','Rectangle','Rectangle and Semi-Circle','Rectangular Prism','Right Triangle','Right Triangles','Scale','Scatter Plots','Shift','Similarity','Sine','Single','Slope and Point','Slope-Intercept Form','Slope-Intercept From','Solving','Solving for y','Special Cases','Sphere','Square','Square & Circle','Square Root Method','Squared','Standard Form','Standard to General Form','Sub & Solve','Sub and Solve','Substitution','System of Inequality','Table','Table to Graph','Tangent','Tangent to axis','Time','Trapezoid','Triangle','Triangle + Kite','Triangle and Circle','Triangular Prism','Trick','Trig','Two-Step','U-Sub','Unit Circle','Unit Conversion','Vertex Form','Vertext Form','Whole','Word Probem','Word Problem','X^4','a:b','a=1','a>1','f(0)','f(a)','f(a)=b','f(x)=0','f(x)=a','x','x-int','x=a','x^4','xi-int','y','y-int','y-value','Combining and Seperating Sentances','Comma Uses and Misuses' ,'Comma Uses-Misuses','Support/Refute']

        self.difficulty = ["Easy","Medium", "Hard", "1","2","3","4","5"]
        self.correctness = {
                "Correct":"1",
                "Incorrect":"0"
                }
        self.section = ["1","2","2E","2H","3","4"]
            
        self.calculator = ["Desmos","TI","Casio","Desmos, TI","Desmos, Casio","Desmos, Casio, TI","Casio, TI"]

    
