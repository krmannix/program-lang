module Interpret where

import AbstractSyntax
import Parse
import TypeCheck

eval :: [(String, Bool)] -> Exp -> Bool
eval env (And e1 e2) = 
	let o = eval env e1
	    p = eval env e2
	in o && p
eval env (Or e1 e2) = 
	let o = eval env e1
	    p = eval env e2
	in o || p
eval env (Not e) = 
	let o = eval env e
	in not o
eval env (Variable v) =
	let c = [b | (v', b) <- env, v' == v]
	in if length c > 0 then head c else False
eval env (Value b) = b


exec :: [(String, Bool)] -> Stmt -> ([(String, Bool)], Output)
exec env (Print    e s) =
  let (env', o) = exec env s
  in (env', [eval env e] ++ o)
exec env  End           = (env, [])
exec env (Assign x e s) = 
	let o = eval env e
	    env' = env ++ [(x, o)]
	in exec env' s

interpret :: Stmt -> Maybe Output
interpret s = if chk [] s == Just Void then 
				let (env, o) = exec [] s 
				in Just o
			  else Nothing

-- eof