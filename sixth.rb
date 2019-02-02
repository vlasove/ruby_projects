i = 0
while i < 5
    puts(i)
    i+=1
end

while true
    puts("lol")
    break

end


x = 1
y = 10
for el in x..y
    puts(el)
end

arr = Array["Bob", "Alex","Georg"]
for a in arr
    puts(a +" is amazing man")
end

for j in 0..arr.length()-1
    puts(arr[j])
end

#strange loop
arr.each do |index|
    puts(index)
end