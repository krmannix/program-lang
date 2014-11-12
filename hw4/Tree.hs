---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
-- Tree.hs
--

-- functionName :: In_type -> Out_type
-- functionName(In_type) = Out_type

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq, Show) -- 1A


twigs :: Tree -> Integer
twigs (Leaf) = 0;
twigs (Twig) = 1;
twigs (Branch b1 b2 b3) = twigs(b1) + twigs(b2) + twigs(b3)

branches :: Tree -> Integer
branches(Leaf) = 0;
branches(Twig) = 0;
branches(Branch b1 b2 b3) = 1 + branches(b1) + branches(b2) + branches(b3);

height :: Tree -> Integer
height(Leaf) = 0;
height(Twig) = 1;
height(Branch b1 b2 b3) = 1 + maximum [height(b1), height(b2), height(b3)];

perfect :: Tree -> Bool
perfect(Leaf) = True;
perfect(Twig) = False;
perfect(Branch b1 b2 b3) = (perfect(b1) && perfect(b2) && perfect(b3)) && (height(b1) == height(b2)) && (height(b2) == height(b3));



--eof