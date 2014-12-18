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
foldTree f (Branch x y)  = f ([foldTree f t | t <- y] ++ [x])

smallest :: Ord a => Tree a -> a
smallest (Finish x) = x
smallest (Branch x y) = minimum ((x : (map smallest y)))

largest :: Ord a => Tree a -> a
largest (Finish x) = x
largest (Branch x y) = maximum ((x : (map largest y)))

data Allocation =
    Alloc [(Var, Register)]
  deriving (Eq, Show)

instance Ord Allocation where
	(Alloc l) <  (Alloc r) = length (nub [r | (v, r) <- l]) >  length (nub [r_ | (v_, r_) <- r])
	(Alloc l) <= (Alloc r) = length (nub [r | (v, r) <- l]) >= length (nub [r_ | (v_, r_) <- r])

--
allocations :: (Interference, [Register]) -> Allocation -> [Var] -> Tree Allocation
allocations (conflicts, rs) (Alloc alloc) (x:xs) = 
	let ca = (Alloc alloc) in
	let ur = unconflicted (conflicts, rs) (Alloc alloc) x
	in if null xs
		then Branch ca [Finish (Alloc (alloc ++ [(x, r)])) | r <- ur]
		else Branch ca [allocations (conflicts, rs) (Alloc (alloc ++ [(x, r)])) (xs) | r <- ur]

{- ALL HELPER FUNCTIONS -}
-- Takes a variable and returns registers it can be used in
unconflicted :: (Interference, [Register]) -> Allocation -> Var -> [Register]
unconflicted (conflicts, rs) (Alloc a) x = rs \\ [r | (y,r) <- a, (x,y) `elem` conflicts || (y,x) `elem` conflicts]

concatAllLeaves :: Tree Allocation -> [Allocation]
concatAllLeaves (Finish   t) = [t]
concatAllLeaves (Branch a t) = concat (map concatAllLeaves t)

getK :: Int -> [Allocation] -> Allocation
getK k allocs = maximum ([Alloc a | (Alloc a) <- allocs, length (nub [r | (_, r) <- a]) <= k])



--eof





