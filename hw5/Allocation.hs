---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Allocation.hs
--

module Allocation where

type Item = Integer
type Bin = Integer

data Alloc = Alloc Bin Bin deriving (Eq, Show)

data Graph =
    Branch Alloc Graph Graph 
  | Finish Alloc
  deriving (Eq, Show)

instance Ord Alloc where
	(Alloc l r) < (Alloc l_ r_) = abs(l-r) < abs(l_-r_)
	(Alloc l r) <= (Alloc l_ r_) = abs(l-r) <= abs(l_-r_)

instance Ord Graph where
	g < g' = alloc(g) < alloc(g')
	g <= g' = alloc(g) <= alloc(g')

leftGraphHelper :: Alloc -> [Item] -> Graph
leftGraphHelper (Alloc l r) i 
	| (length i) == 1 = Finish (Alloc (head i + l) r)
	| otherwise = Branch (Alloc (head i + l) r) (leftGraphHelper (Alloc (head i + l) r) (snd (splitAt 1 i))) (rightGraphHelper (Alloc (head i + l) r) (snd (splitAt 1 i))) 

rightGraphHelper :: Alloc -> [Item] -> Graph
rightGraphHelper (Alloc l r) i
	| (length i) == 1 = Finish (Alloc l (head i + r))
	| otherwise = Branch (Alloc l (head i + r)) (leftGraphHelper (Alloc l (head i + r)) (snd (splitAt 1 i))) (rightGraphHelper (Alloc l (head i + r)) (snd (splitAt 1 i))) 

finalHelper :: Graph -> [Alloc] -> [Alloc]
finalHelper (Branch a l r) i = (finalHelper l i) ++ (finalHelper r i) ++ i
finalHelper (Finish a) i = i ++ [a]

depthHelper :: Integer -> Integer -> Graph -> [Alloc] -> [Alloc]
depthHelper c n (Branch a l r) i 
	| c == n = i ++ [a]
	| c > n = []
	| otherwise = (depthHelper (c+1) n l i) ++ (depthHelper (c+1) n r i) ++ i
depthHelper c n (Finish a) i 
	| c == n = i ++ [a]
	| otherwise = i

graph :: Alloc -> [Item] -> Graph
graph a i 
	| (length i) == 0 = Finish a
	| otherwise = Branch a (leftGraphHelper a i) (rightGraphHelper a i)

alloc :: Graph -> Alloc
alloc (Branch a _ _) = a
alloc (Finish a) = a

final ::  Graph -> [Alloc]
final (Branch a l r) = finalHelper (Branch a l r) []
final (Finish a) = [a]

depth :: Integer -> Graph -> [Alloc]
depth n g = depthHelper 0 n g []

type Strategy = Graph -> Graph



--eof