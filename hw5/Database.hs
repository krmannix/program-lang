---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Database.hs
--

module Database where
import Data.List (nub, reverse)

type Column = String
data User = User String deriving (Eq, Show)
data Table = Table String deriving (Eq, Show)
data Command =
    Add User
  | Create Table
  | Allow (User, Table)
  | Insert (Table, [(Column, Integer)])
  deriving (Eq, Show)

example = [
    Add (User "Alice"),
    Add (User "Bob"),
    Create (Table "Revenue"),
    Insert (Table "Revenue", [("Day", 1), ("Amount", 2400)]),
    Insert (Table "Revenue", [("Day", 2), ("Amount", 1700)]),
    Insert (Table "Revenue", [("Day", 3), ("Amount", 3100)]),
    Allow (User "Alice", Table "Revenue")
  ]

-- Useful function for retrieving a value from a list
-- of (label, value) pairs.
lookup' :: Column -> [(Column, Integer)] -> Integer
lookup' c' ((c,i):cvs) = if c == c' then i else lookup' c' cvs

-- ALL HELPER METHODS
-- See if table exists
tableExists :: Table -> [Command] -> Bool
tableExists t c = length [() | n <- [n | Create(n) <- c], n == t] > 0--Create (t) == Create (Table "Revenue") --length [(t) | Create (t) <- c]

userPermission :: User -> Table -> [Command] -> Bool
userPermission u t c = length [() | (u_, t_) <- [(u_, t_) | Allow (u_, t_) <- c], u_ == u && t_ == t] > 0

userExists :: User -> [Command] -> Bool
userExists u c = length [() | u_ <- [u_ | Add (u_) <- c], u_ == u] > 0

selectFromTable :: Table -> Column -> [Command] -> [Integer]
selectFromTable t l c = [v | (l_, v) <- concat[f | Insert (t_, f) <- c, t_ == t ], l_ == l]

checkUserCreated :: [Command] -> User -> Bool
checkUserCreated c u = length [() | Add (u_) <- c, u_ == u] > 0

checkTableCreated :: [Command] -> Table -> Bool
checkTableCreated c t = length [() | Create (t_) <- c, t_ == t] > 0

isCreated :: [Command] -> Command -> Bool
isCreated c (Allow (u, t)) = (checkUserCreated c u) && (checkTableCreated c t)
isCreated c (Insert (t, _)) = (checkTableCreated c t)
isCreated c _ = True

validateHelper :: [Command] -> Bool
validateHelper c = if (length c) > 1 -- then if isCreated (concat((splitAt 1 c) !! 1)) (((splitAt 1 c) !! 0) !! 0) then True else False else False
                    then 
                      if checkIsCreated (splitAt 1 c)
                        then validateHelper (snd (splitAt 1 c))
                      else 
                        False
                  else
                    if (length c) == 0
                      then 
                        False
                    else -- Means length == 1
                      isCreated [] (head c)

checkIsCreated :: ([Command], [Command]) -> Bool
checkIsCreated (l, c) = isCreated c (head l)

-- REAL FUNCTIONS

-- Complete for Assignment 5, Problem 1, part (a).
select :: [Command] -> User -> Table -> Column -> Maybe [Integer]
select c u t l = if tableExists t c && userExists u c && userPermission u t c
                    then Just (selectFromTable t l c)
                    else Nothing

-- Type synonym for aggregation operators.
type Operator = Integer -> Integer -> Integer

-- Complete for Assignment 5, Problem 1, part (b).
aggregate :: [Command] -> User -> Table -> Column -> Operator -> Maybe Integer
aggregate c u t l o = if tableExists t c && userExists u c && userPermission u t c
                        then Just (foldr o 0 (selectFromTable t l c))
                        else Nothing


-- Complete for Assignment 5, Problem 1, part (c).
validate :: [Command] -> Bool
validate c = validateHelper (reverse c)



--eof