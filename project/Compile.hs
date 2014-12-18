module Compile where

import AbstractSyntax
import Allocation
import Machine
import TypeCheck

class Compilable a where
  comp :: [(Var, Register)] -> a -> Instruction

instance Compilable Stmt where
  comp xrs (End)          = STOP (Register 0)
  comp xrs (Print    e s) = COPY (Register 0) (register (comp xrs e)) (comp xrs s)
  comp xrs (Assign x e s) = COPY (lookup' x xrs) (register (comp xrs e)) (comp xrs s)

instance Compilable Exp where
  comp xrs (Variable x) = STOP (lookup' x xrs)
  comp xrs (Value False) = 
  	   let x = (maximum [y | (_, y) <- xrs]) + 1
  	in INIT (x) (STOP x)
  comp xrs (Value True) =
  	   let x = (maximum [y | (_, y) <- xrs]) + 1
  	in INIT (x) (FLIP (x) (STOP x))
  comp xrs (And e1 e2) =
  	   let x = (maximum [y | (_, y) <- xrs]) + 1
  	in let l = comp (("_",  x    ):xrs) e1
  	in let r = comp (("__", x + 1):xrs) e2
  	in NAND (register l) (register r) x (FLIP x (STOP x))
  comp xrs (Or e1 e2) = 
  	   let x = (maximum [y | (_, y) <- xrs]) + 1
  	in let l = comp (("_",  x    ):xrs) e1
  	in let r = comp (("__", x + 1):xrs) e2
  	in FLIP (register l) (FLIP (register r) (NAND (register l) (register r) x (STOP x)))
  comp xrs (Not    v) = 
  	   let x = register (comp xrs v) --(maximum [y | (_, y) <- xrs]) + 1
  	in FLIP (x) (STOP x)

compileMin :: Stmt -> Maybe Instruction
compileMin s =
  if chk [] s == Just Void then
       let unboundVars = unbound s 
    in let numUnbound  = [(Register (toInteger x)) | x <- [0..length unboundVars]]
    in let interferenceVars = interference s
    in let Alloc x = smallest (allocations (interferenceVars, numUnbound) (Alloc []) unboundVars)
    in Just (comp x s)
  else Nothing

compileMax :: Integer -> Stmt -> Maybe Instruction
compileMax k s =  
  if chk [] s == Just Void then
       let unboundVars = unbound s 
    in let numUnbound  = [(Register (toInteger x)) | x <- [0..length unboundVars]]
    in let interferenceVars = interference s
    in let allocs = concatAllLeaves (allocations (interferenceVars, numUnbound) (Alloc []) unboundVars)
    in let (Alloc fa) = getK (fromInteger k) allocs
    in Just (comp fa s)
  else Nothing

-- eof
