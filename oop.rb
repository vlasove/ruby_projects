class Car
    attr_accessor :speed, :model, :color

    def initialize(speed, model, color)
        @speed = speed
        @color = color
        @model = model
    end
end


audi = Car.new(220, "sx","gray")

puts("#{audi.speed}"+" "+audi.model+" "+audi.color)

