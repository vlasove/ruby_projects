age = 35
puts(age)
age+=1
puts(age)

name = 'Hi all, want some stuff?'
puts(name)

keks = 0.98
what = true
none = nil

puts (what)

puts(none)

#String type
words = "Our \"web\" projects"
puts (words.downcase() +" "+name)

text = "     LolKek    "
puts(text.strip().length())
puts(text.include?'o')


#Int counts
x = 5
y = 2
res = x+y*x
res2 = x**y

puts(res)
puts(res2)
puts("Our result is: "+ (res2 % (x+1)).to_s )

numAbs = -14.45
puts(numAbs.abs())
puts(numAbs.round())

puts(Math.sqrt(144).to_i)