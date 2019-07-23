// TODO : j = 0, not j = 1, fix the f(x), f[x], f_x notation
// maybe normalize the section names
// also, make some sections less wordy
// fix the awful title tags for all sites
// does dp[] become d[]?
// replace lli with long long in code ?

#site-title 1D1D DP: A Dynamic Programming Optimization

#latex-preamble
$$
	\DeclareMathOperator*{\argmax}{argmax}
	\DeclareMathOperator*{\value}{value}
	\DeclareMathOperator*{\opt}{opt}
$$
#end latex-preamble

#title 1D1D DP: A Dynamic Programming Optimization
#warning
#toc

// End preamble

#main

#section General Form
In the motivation problem, there are $ O(N) $ states, each relying on $ O(N) $ previous states. This is where the name "1D1D" comes from: 1 dimension of states, each relying on one dimension of previous states. All 1D1D DP recurrences follow the form of

#block General Form
	$$ dp[i] = \max_{j = 0}^{i - 1} \left[ d_j + f(i, j) \right] $$
#end block

#code 123-456
using namespace std;
using namespace std;
using namespace std;
#end code

Note that depending on the problem and implementation, $ max $ may be replaced with $ min $ and $ j = 0 $ might instead be $ j = 1 $.

The function $ f(i, j) $ represents a cost or weight function in minimization problems and a value or utility function in maximization problems. In the motivation problem, $ f(i, j) = A(p[i] - p[j])^2 + B(p[i] - p[j]) + C $.
#end section

#end main
