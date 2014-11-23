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

leftGraphHelper :: Alloc -> [Item] -> Graph
leftGraphHelper (Alloc l r) i 
	| (length i) == 1 = Finish (Alloc (head i + l) r)
	| otherwise = Branch (Alloc (head i + l) r) (leftGraphHelper (Alloc (head i + l) r) (snd (splitAt 1 i))) (rightGraphHelper (Alloc (head i + l) r) (snd (splitAt 1 i))) 

rightGraphHelper :: Alloc -> [Item] -> Graph
rightGraphHelper (Alloc l r) i
	| (length i) == 1 = Finish (Alloc l (head i + r))
	| otherwise = Branch (Alloc l (head i + r)) (leftGraphHelper (Alloc l (head i + r)) (snd (splitAt 1 i))) (rightGraphHelper (Alloc l (head i + r)) (snd (splitAt 1 i))) 

graph :: Alloc -> [Item] -> Graph
graph a i 
	| (length i) == 0 = Finish a
	| otherwise = Branch a (leftGraphHelper a i) (rightGraphHelper a i)

type Strategy = Graph -> Graph



--eof