File.open("text/simple.txt","r") do |j|
    #puts(j.readline().upcase())

    for line in j.readlines()
        puts(line)
    end
end


file = File.open("text/simple.txt","r")
puts(file.read())


File.open("text/simple.txt","a") do |j|
    j.write("Kekkekkek")
end


File.open("text/index.html","a") do |file|
    file.write("<h1>Hello Web!!</h1>")
end

