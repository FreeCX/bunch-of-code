module Main where

import Data.Maybe (fromJust)
import Data.List (elemIndex)
import Data.Char (ord, chr)
import Text.Printf (printf)

alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#@"

-- добавление паддинга до размера size
sizePadding :: ([a] -> [a] -> [a]) -> Int -> a -> [a] -> [a]
sizePadding func size value array
  | curr > size = error $ "Current size > " ++ (show size)
  | curr < size = func array padding
  | otherwise = array
  where
    -- размер входных данных
    curr = length array
    -- размер паддинга
    padsize = size - curr
    -- сам паддинг
    padding = take padsize $ repeat value

-- добавление паддинга до кратного modBy
modPadding :: ([a] -> [a] -> [a]) -> Int -> a -> [a] -> [a]
modPadding func modBy value array = func array padding where
  -- размер входных данных
  modv = (length array) `mod` modBy
  -- размер паддинга
  padsize = if modv == 0 then 0 else modBy - modv
  -- паддинг
  padding = take padsize $ repeat value

-- удаление паддинга с конца массива
removePadding :: Int -> [Int] -> [Int]
removePadding size arr = take wop arr where
  len = length arr 
  wop = len - (len `mod` size)

-- группировка данных по n элементов
group :: Int -> [Int] -> [[Int]]
group _ [] = []
group n l 
  | n > 0 = (take n l) : (group n $ drop n l)
  | otherwise = error "Negative or zero n"

-- преобразование массива битов в число
asInt :: [Int] -> Int
asInt = foldl (\a b -> (a * 2) + b) 0

-- преобразование строки в массив int`ов
toIntMap :: (Char -> [Int]) -> String -> [Int]
toIntMap func = foldr (++) [] . map func

-- преобразование int в бинарное представление
binary :: Int -> [Int]
binary = convert [] where
  convert arr 0 = arr
  convert arr val = convert ((: arr) . (`mod` 2) $ val) (val `div` 2)

-- кодирование
encode :: String -> String
encode = asAlphabet . group 6 . modTail6 . toIntMap asArray8 where
  -- преобразование индекса в символ алфавита
  asAlphabet = map ((alphabet !!) . asInt)
  -- добавление паддинга в начало
  headPad8 = sizePadding (\a b -> b ++ a) 8 0
  -- добавление паддинга в конце
  modTail6 = modPadding (++) 6 0
  -- строка в набор бит
  asArray8 = headPad8 . binary . ord

-- декодирование
decode :: String -> String
decode = asAlphabet . group 8 . removePadding 8 . toIntMap asArray6 where
  -- преобразование индекса в символ
  asAlphabet = map (chr . asInt)
  -- добавление паддинга в начало
  headPad6 = sizePadding (\a b -> b ++ a) 6 0
  -- строка в набор бит
  asArray6 = headPad6 . binary . fromJust . (`elemIndex` alphabet)

main = do
  input <- getLine
  let encoded = encode input
  let decoded = decode encoded
  printf " input: `%s`\nencode: `%s`\ndecode: `%s`\n" input encoded decoded
