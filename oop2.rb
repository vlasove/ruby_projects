class Transport
    attr_accessor :color, :wheels
    def initialize(color, wheels)
        @color = color
        @wheels = wheels

    end

    def sayBip()
        puts("BipMfka")
    end
    
end


class Cars < Transport
    attr_accessor :isMechanic
    
end

bike = Transport.new("blue",2)
car = Transport.new("red", 4)