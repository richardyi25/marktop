#!/usr/bin/python3
from sys import argv
argc = len(argv)

# Help message
def print_help():
	print("Usage: python3 marktop.py [Marktop source file] [HTML destination]")
	print("Example: python3 marktop.py file.mt file.html")
	raise SystemExit

# Incorrect number of arguments supplied
if argc != 3:
	print("Invalid number of arguments.")
	print_help()

# Unpack argv
program, input_filename, output_filename = argv

# Global site information
site_title = ""
latex_preamble = []
title = ""
do_warning = False
do_toc = False
sections = []
section_titles = []
current_section = []
current_block = []
current_code = []
current_latex = ""

body_start = """
<html lang="en">
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta charset="UTF-8">
		<title>%s</title>
		<link rel="stylesheet" href="prism.css">
		<link rel="stylesheet" href="../style.css">
		<link rel="stylesheet" href="local_style.css">
		<script type="text/x-mathjax-config">
			MathJax.Hub.Config({
				tex2jax: {
					inlineMath: [['$','$']],
					displayMath: [['$$','$$']],
					processEscapes: true
				}
			});
		</script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML" async></script>
		<script src="prism.js"></script>
	</head>

	<body>
""".strip('\n')

title_text = """
		<div id="title">%s</div>
""".strip('\n')

body_end = """
	</body>
</html>
""".strip('\n')

preamble_start = """
		<div id="preamble">
""".strip('\n')

preamble_end = """
		</div>
""".strip('\n')

warning_text = """
		<div id="warning">
			<div class="subheading">Warning: This article is not finished</div>
			This article is still being written and edited. There are most likely many mistakes and typos.
		</div>
""".strip('\n')

toc_start = """
		<div id="toc">
			<div class="heading">Table of Contents</div>
			<ul>
""".strip('\n')

toc_end = """
			</ul>
		</div>
""".strip('\n')

toc_item = """
				<li><a href="#toc%d">%s</a></li>
""".strip('\n')

main_start = """
		<div id="main">
""".strip('\n')

main_end = """
		</div>
""".strip('\n')

section_start = """
			<div id="toc%d" class="section">
				<div class="heading">%s</div>
				<div class="subsection">
""".strip('\n')

section_end = """
				</div>
			</div>
""".strip('\n')

block_start = """
					<div class="block">
						<div class="block-heading">%s</div>
""".strip('\n')

block_end = """
					</div>
""".strip('\n')

code_start = """
					<pre class="line-numbers" data-line="%s"><code class="language-cpp">
""".strip('\n')

code_end = """
</code></pre>
""".strip('\n')

def make_preamble(preamble):
	return preamble_start + '\n' + '\n'.join(map(lambda line: '\t\t\t\t' + line, preamble)) + '\n' + preamble_end

def make_toc_item(title, which):
	return toc_item % (which, title)

def make_toc(titles):
	result = toc_start + '\n'
	for i in range(len(titles)):
		title = titles[i]
		result += make_toc_item(title, i) + '\n'
	return result + toc_end

def make_part(part):
	if part[0] == '<' or part[0] == '\t':
		return '\n' + part
	else:
		return '\n\t\t\t\t\t<p>\n\t\t\t\t\t\t' + part + '\n\t\t\t\t\t</p>'

def make_supersection(name):
	return '\t\t\t<div class="part">' + name + '</div>'

def make_section(section, which):
	title = section[0]
	parts = section[1:]
	parts = map(make_part, parts)
	return section_start % (which, title) + '\n' + '\n'.join(parts) + '\n' + section_end

def make_block(block):
	title = block[0]
	parts = block[1:]
	parts = map(make_part, parts)
	return block_start % title + '\n' + '\n'.join(parts) + '\n' + block_end

def make_code(code):
	title = code[0]
	parts = code[1:]
	parts_text = '\n'.join(parts)
	escaped = ''
	for ch in parts_text:
		if ch == '<':
			escaped += '&lt;'
		elif ch == '>':
			escaped += '&gt;'
		elif ch == '&':
			escaped += '&amp;'
		else:
			escaped += ch
	return code_start % title + escaped + code_end

# Parsing flags
latex_preamble_flag = False
main_flag = False
section_flag = False
block_flag = False
code_flag = False
latex_flag = False

# Parse Marktop file
with open(input_filename, "r") as input_file:
	# Breaks on LF-only systems
	input_lines = input_file.read().split("\n")

	input_length = len(input_lines)
	line_number = 0
	while line_number < input_length:
		line = input_lines[line_number].rstrip()

		# Process text only if it's not code
		if not code_flag:
			# Skip empty lines
			if line == "":
				line_number += 1
				continue

			# Removing leading tabs
			line = line.lstrip('\t')
			
			# Skip comment lines (starting with //)
			if len(line) >= 2 and line[:2] == '//':
				line_number += 1
				continue

		# Split into first word, and the rest, by space
		tokens = line.split(" ", 1)
		first = tokens[0]
		if len(tokens) > 1:
			rest = tokens[1]

		# Parsing LaTeX preamble
		if latex_preamble_flag:
			if first == "#end":
				latex_preamble_flag = False
			else:
				latex_preamble.append(line)

		elif main_flag:
			if section_flag:
				if latex_flag:
					if line.strip() == "$$":
						latex_flag = False
						line = current_latex + "$$"
						#current_latex = ""
					else:
						current_latex += line
						line_number += 1
						continue
				else:
					if line.strip() == "$$":
						latex_flag = True
						current_latex = line
						line_number += 1
						continue

				if block_flag:
					if first == "#end":
						block_flag = False
						current_section.append(make_block(current_block))
					else:
						current_block.append(line)

				elif first == "#block":
					block_flag = True
					current_block = [rest]

				elif code_flag:
					if first == "#end":
						code_flag = False
						current_section.append(make_code(current_code))
					else:
						current_code.append(line)

				elif first == "#code":
					code_flag = True
					current_code = [rest]

				elif first == "#end":
					section_flag = False
					section_titles.append(current_section[0])
					sections.append(make_section(current_section, len(sections)))

				else:
					current_section.append(line)

			elif first == "#section":
				section_flag = True
				current_section = [rest]

			elif first == "#part":
				sections.append(make_supersection(rest))

			elif first == "#end":
				main_flag = False

		# Control sequences that start with #
		elif first == "#site-title":
			site_title = rest

		elif first == "#latex-preamble":
			latex_preamble_flag = True
			line_number += 1
			continue

		elif first == "#title":
			title = rest

		elif first == "#warning":
			do_warning = True

		elif first == "#toc":
			do_toc = True

		elif first == "#main":
			main_flag = True

		line_number += 1

with open(output_filename, "w") as output_file:
	output_file.write(body_start % site_title + '\n')

	output_file.write(title_text % title + '\n\n')

	if len(latex_preamble) > 0:
		output_file.write(make_preamble(latex_preamble) + '\n\n')

	if do_warning:
		output_file.write(warning_text + '\n\n')
	
	if do_toc:
		output_file.write(make_toc(section_titles) + '\n\n')

	output_file.write(main_start + '\n\n')

	for section in sections:
		output_file.write(section + '\n\n')

	output_file.write(main_end + '\n')
	output_file.write(body_end)
