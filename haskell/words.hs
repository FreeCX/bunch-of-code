module Main where

import qualified System.Environment as E
import qualified Data.List as L

main = do
  app <- E.getProgName
  args <- E.getArgs
  case args of
    [file] -> do
      text <- readFile file
      process text
    _ -> printUsage app

-- функция обработка теста
-- 1. разделяем по пробелу и символу перевода строки
-- 2. делаем подсчёт слов
-- 3. выводим статистику
process :: String -> IO ()
process = stat . count . words

-- функция подсчёта количества слов
-- 1. убираем пустые токены
-- 2. сортируем и группируем
-- 3. объединяем одинаковые
count :: [String] -> [(Int, String)]
count = join . L.group . L.sort . filterByLen
  where
    filterByLen = filter ((> 0) . length)
    join = map (\x -> (length x, x !! 0))

-- функция вывода статистики
-- 1. сортируем по убыванию
-- 2. выводим по одному элементу
stat :: [(Int, String)] -> IO ()
stat = mapM_ printItem . L.sortOn reverseOrderFst
  where reverseOrderFst = \(a, _) -> -a

-- функция вывода справочной информации
printUsage :: String -> IO ()
printUsage app = putStrLn $ "usage:\n  " ++ app ++ " <text file>"

-- вывод одного элемента в виде: <количество>: <слово>
printItem :: (Int, String) -> IO ()
printItem (a, b) = putStrLn $ show a ++ ": " ++ b
