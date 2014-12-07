module Interpret where

import AbstractSyntax
import Parse
import TypeCheck

eval :: [(String, Bool)] -> Exp -> Bool
eval env (And e1 e2) = 
	let (env', o) = eval env e1
	let (env'', p) = eval env' e2
	o && p
eval env (Or e1 e2) = 
	let (env', o) = eval env e1
	let (env'', p) = eval env' e2
	o || p
eval env (Not e) = 
	let (env', o) = eval env e
	not o
eval _ _ = False -- Implement for Problem #1, part (b).


exec :: [(String, Bool)] -> Stmt -> ([(String, Bool)], Output)
exec env (Print    e s) =
  let (env', o) = exec env s
  in (env', [eval env e] ++ o)
exec env (End _) = (env, [])
exec env (Assign x e s) = 
	let (env', o) = eval env e
	in (env' ++ (x, o), [exec env s])
exec env _ = (env, []) -- Implement the Assign and End cases for Problem #1, part (b).

interpret :: Stmt -> Maybe Output
interpret s = if typeOf (chk [] s) == Just Void then Maybe interpret [] s else Nothing
interpret _ = Nothing -- Implement for Problem #1, part (d).

-- eof