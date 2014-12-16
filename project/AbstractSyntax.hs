module AbstractSyntax where

import Data.List (union, intersect, (\\), nub)

type Var = String
type Output = [Bool]

data Stmt =
    Print Exp Stmt
  | Assign Var Exp Stmt
  | End
  deriving (Eq, Show)

data Exp =
    Variable Var
  | Value Bool
  | And Exp Exp
  | Or Exp Exp
  | Not Exp
  deriving (Eq, Show)

data Type =
    Bool
  | Void
  deriving (Eq, Show)

-- Useful helper functions.
lookup' :: Eq a => a -> [(a, b)] -> b
lookup' x ((x',i) : rest) = if x == x' then i else lookup' x rest

-- Type class for a polymorphic fold function on abstract syntax trees.
--
--  * The first argument is the aggregator for combining
--    results of recursive folds.
--  * The second argument is a function that will be applied to
--    (i.e., and will replace) Variable nodes.
--  * The third argument is a constant that will replace all
--    non-Variable leaf nodes (i.e., Value nodes).
--  * The fourth argument is the abstract syntax tree that
--    will be folded.

class Foldable b where
  fold :: ([a] -> a) -> (String -> a) -> a -> b -> a

instance Foldable Exp where
  fold f var b (Variable x ) = var x
  fold f var b (Value v    ) = b
  fold f var b (And   e1 e2) = f [fold f var b e1, fold f var b e2]
  fold f var b (Or    e1 e2) = f [fold f var b e1, fold f var b e2]
  fold f var b (Not   e    ) = f [fold f var b e]

instance Foldable Stmt where
  fold f var b (Print    e s) = f [fold f var b e, fold f var b s] -- Finish this definition for Problem #2, part (a).
  fold f var b (Assign x e s) = f [var x, fold f var b e, fold f var b s]
  fold f var b (End)          = b

  

class HasVariables a where
  vars :: a -> [Var]

instance HasVariables Stmt where
  --vars (Print    e s) = fold [] (++) e s
  vars _ = [] -- Implement for Problem #2, part (a).

instance HasVariables Exp where
  vars _ = [] -- Implement for Problem #2, part (a).



unbound :: Stmt -> [Var]
unbound End = []
unbound (Print    e s) = unboundExp e `union` unbound s
unbound (Assign x e s) = unboundExp e `union` (unbound s \\ [x])

unboundExp :: Exp -> [Var]
unboundExp (Variable x ) = [x]
unboundExp (Value    v ) = []
unboundExp (And   e1 e2) = (unboundExp e1) ++ (unboundExp e2)
unboundExp (Or    e1 e2) = (unboundExp e1) ++ (unboundExp e2)
unboundExp (Not   e    ) = unboundExp e




type Interference = [(Var, Var)]

interference :: Stmt -> Interference
interference End = []
interference (Print    e s) = interference s
interference (Assign x e s) = [ (x_, y_) | (x_, y_) <- (interference s), x_ /= y_, y_ `elem` (unbound s), y_ `elem` (unboundExp e)]


-- eof