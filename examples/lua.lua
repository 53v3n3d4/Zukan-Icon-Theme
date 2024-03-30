-- from lua.org

print(type("Hello world"))  --> string
print(type(10.4*3))         --> number
print(type(print))          --> function
print(type(type))           --> function
print(type(true))           --> boolean
print(type(nil))            --> nil
print(type(type(X)))        --> string


a, b, c = 0, 1
print(a,b,c)           --> 0   1   nil
a, b = a+1, b+1, b+2   -- value of b+2 is ignored
print(a,b)             --> 1   2
a, b, c = 0
print(a,b,c)           --> 0   nil   nil

if op == "+" then
  r = a + b
elseif op == "-" then
  r = a - b
elseif op == "*" then
  r = a*b
elseif op == "/" then
  r = a/b
else
  error("invalid operation")
end

-- print all keys of table `t'
for k in pairs(t) do print(k) end

-- add all elements of array `a'
function add (a)
  local sum = 0
  for i,v in ipairs(a) do
    sum = sum + v
  end
  return sum
end

t = {10, 20, 30}
iter = list_iter(t)    -- creates the iterator
while true do
  local element = iter()   -- calls the iterator
  if element == nil then break end
  print(element)
end

co = coroutine.create(function ()
       for i=1,10 do
         print("co", i)
         coroutine.yield()
       end
     end)

mt = {}          -- create the matrix
for i=1,N do
  mt[i] = {}     -- create a new row
  for j=1,M do
    mt[i][j] = 0
  end
end

local authors = {}      -- a set to collect authors
function Entry (b) authors[b[1]] = true end
dofile("data")
for name in pairs(authors) do print(name) end

Account = {balance = 0}

function Account:new (o)
  o = o or {}
  setmetatable(o, self)
  self.__index = self
  return o
end

function Account:deposit (v)
  self.balance = self.balance + v
end

function Account:withdraw (v)
  if v > self.balance then error"insufficient funds" end
  self.balance = self.balance - v
end

static int l_sin (lua_State *L) {
  double d = lua_tonumber(L, 1);  /* get argument */
  lua_pushnumber(L, sin(d));  /* push result */
  return 1;  /* number of results */
}
