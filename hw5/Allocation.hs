---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Allocation.hs
--

{-  

	DATA

 -}

module Allocation where
import Data.Function
import Data.List

type Item = Integer
type Bin = Integer

data Alloc = Alloc Bin Bin deriving (Eq, Show)

data Graph =
    Branch Alloc Graph Graph 
  | Finish Alloc
  deriving (Eq, Show)

type Strategy = Graph -> Graph

instance Ord Alloc where
	(Alloc l r) < (Alloc l_ r_) = abs(l-r) < abs(l_-r_)
	(Alloc l r) <= (Alloc l_ r_) = abs(l-r) <= abs(l_-r_)

instance Ord Graph where
	g < g' = alloc(g) < alloc(g')
	g <= g' = alloc(g) <= alloc(g')

{-  

	ALL HELPER FUNCTIONS

 -}

isNonEmpty :: [Item] -> Bool
isNonEmpty i = null i

longerThan :: Int -> [Item] -> Bool
longerThan n xs = isNonEmpty $ drop n xs

leftGraphHelper :: Alloc -> [Item] -> Graph
leftGraphHelper (Alloc l r) i 
	| longerThan 1 i = Finish (Alloc (head i + l) r)
	| otherwise = Branch (Alloc (head i + l) r) (leftGraphHelper (Alloc (head i + l) r) (snd (splitAt 1 i))) (rightGraphHelper (Alloc (head i + l) r) (snd (splitAt 1 i))) 

rightGraphHelper :: Alloc -> [Item] -> Graph
rightGraphHelper (Alloc l r) i
	| longerThan 1 i = Finish (Alloc l (head i + r))
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

patientHelper :: Integer -> Integer -> Strategy
patientHelper c n (Branch a l r)
	| c == n-1 = if l < r then l else r
	| otherwise = if patientHelper (c+1) n l < patientHelper (c+1) n r then patientHelper (c+1) n l else patientHelper (c+1) n r

metaRepeatHelper :: Integer -> Integer -> Strategy -> Strategy
metaRepeatHelper c n s1 g 
	| c == n = s1 g
	| otherwise = s1 (metaRepeatHelper (c+1) n s1 g)

fitHelper :: Graph -> Strategy -> Alloc
fitHelper g s = alloc (s g)

{-  

	ALL BASELINES FUNCTIONS

 -}

graph :: Alloc -> [Item] -> Graph
graph a i 
	| null i = Finish a
	| otherwise = Branch a (leftGraphHelper a i) (rightGraphHelper a i)

alloc :: Graph -> Alloc
alloc (Branch a _ _) = a
alloc (Finish a) = a

final ::  Graph -> [Alloc]
final (Branch a l r) = finalHelper (Branch a l r) []
final (Finish a) = [a]

depth :: Integer -> Graph -> [Alloc]
depth n g = depthHelper 0 n g []

greedy :: Strategy
greedy (Branch a l r)
	| l < r = l
	| otherwise = r 
greedy (Finish a) = Finish a

patient :: Integer -> Strategy
patient n (Branch a l r) 
	| n == 0 = Branch a l r
	| otherwise = patientHelper 0 n (Branch a l r)
patient n (Finish a) = Finish a

optimal :: Strategy
optimal (Branch a l r) = if optimal l < optimal r then optimal l else optimal r
optimal (Finish a) = Finish a

metaCompose :: Strategy -> Strategy -> Strategy
metaCompose s1 s2 g = s2 (s1 g)

metaRepeat :: Integer -> Strategy -> Strategy 
metaRepeat n s1 g 
	| n == 0 = g
	| n > 0 = metaRepeatHelper 1 n s1 g

metaGreedy :: Strategy -> Strategy -> Strategy
metaGreedy s1 s2 g = greedy (Branch (Alloc 0 0) (s1 g) (s2 g))

impatient :: Integer -> Strategy
impatient n g = (metaRepeat n greedy) g

{-  

	ANSWER TO PART G:

	patient looks through each possible ending node at depth n, and will give the best
	possible outcome at that depth - when using the patient algorithm, we can be assured
	that we will receive the best scenario for allocation. In this way, patient is superior to 
	impatient

	impatient is a greedy algorithm repeated many times, meaning at each step it makes a hyperlocal
	decision at each node. In this way, impatient is a much faster algorithm than patient (and becomes faster
	relative to patient with each increasing number of n) as it iteratively goes through each level of a graph - the lookup 
	time for patient is around nlogn, while for impatient it is n, if n == depth. While it is fast, the end result may not 
	necessarily be the best algorithm at that depth, as a "good" greedy decision at a node may lead to a "worse" result 
	in the long term. However, it is superior to patient in terms of speed and calculation time.

 -}

{-  

	EXTRA CREDIT BASELINE FUNCTION

 -}

fit :: Graph -> [Strategy] -> Strategy
fit g i = minimumBy (compare `on` (fitHelper g)) i




--eof