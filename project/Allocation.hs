module Allocation where

import Data.List (union, intersect, (\\), nub)
import AbstractSyntax
import Machine

data Tree a =
    Branch a [Tree a]
  | Finish a
  deriving (Eq, Show)

foldTree :: ([a] -> a) -> Tree a -> a
foldTree f (Finish x) = x
foldTree f (Branch x (y:ys))  = foldTree f y 	--FINISH THIS

smallest :: Ord a => Tree a -> a
smallest (Finish x) = x
smallest (Branch x y) = minimum ((x : (map smallest y)))

largest :: Ord a => Tree a -> a
largest (Finish x) = x
largest (Branch x y) = maximum ((x : (map smallest y)))

data Allocation =
    Alloc [(Var, Register)]
  deriving (Eq, Show)

instance Ord Allocation where
	(Alloc l) <  (Alloc r) = length (nub [r | (v, r) <- l]) >  length (nub [r_ | (v_, r_) <- r])
	(Alloc l) <= (Alloc r) = length (nub [r | (v, r) <- l]) >= length (nub [r_ | (v_, r_) <- r])

allocations :: (Interference, [Register]) -> Allocation -> [Var] -> Tree Allocation
allocations (conflicts, rs) (Alloc a) (x:xs) = ??? -- Complete for Problem #3, part (d).

-- Useful helper function.
-- Takes a variable and returns registers it can be used in
unconflicted ::(Interference, [Register]) -> Allocation -> Var -> [Register]
unconflicted (conflicts, rs) (Alloc a) x = rs \\ [r | (y,r) <- a, (x,y) `elem` conflicts || (y,x) `elem` conflicts]

--eof