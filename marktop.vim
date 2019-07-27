syn match Type '#.\{-}\ ' containedin=Statement
syn match Type '#[^\ ]\{-}\n' containedin=Statement

syn match Statement '#.\+'

syn region String start='\$' end='\$'
syn region String start='\$\$' end='\$\$'

syn region Macro start='#code.*\n' end='#end code'

syn match Comment '//.*'
