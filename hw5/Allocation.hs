---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Allocation.hs
--

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

instance Ord Alloc where
	(Alloc l r) < (Alloc l_ r_) = abs(l-r) < abs(l_-r_)
	(Alloc l r) <= (Alloc l_ r_) = abs(l-r) <= abs(l_-r_)

instance Ord Graph where
	g < g' = alloc(g) < alloc(g')
	g <= g' = alloc(g) <= alloc(g')

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

--fitHelper :: Strategy -> Integer
--fitHelper  (Branch (Alloc l r) _ _) _ = abs(l-r)
--fitHelper  (Finish (Alloc l r)) _ = abs(l-r)

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

type Strategy = Graph -> Graph

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

--fit :: Graph -> [Strategy] -> Strategy
--fit g i = minimumBy (compare `on` (fitHelper g)) i



--eof