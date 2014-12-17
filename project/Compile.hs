module Compile where

import AbstractSyntax
import Allocation
import Machine

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

--compileMin :: Stmt -> Maybe Instruction
--compileMin _ = STOP (Register -1) -- Complete for Problem #4, part (c).

--compileMax :: Integer -> Stmt -> Maybe Instruction
--compileMax _ _ = Nothing -- Complete for Problem #4, part (d).

-- eof
