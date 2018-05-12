import os

lineWrites = int(1)

for file in os.listdir('/home/marknolledo/CC/training/cataract/negative/img'):
    filepath = '/'.join(['/home/marknolledo/CC/training/cataract/negative/img', file])
    print("Reading ", filepath)
    
    disorder = str("Normal")
    
    print(disorder, "\nWriting into dataset...")

    #Write into dataset
    with open('categories.csv', 'a') as dataset:
        dataset.write(disorder)
        dataset.write("\n")

    lineWrites+=1

print("Writing complete!\nLines written: ", lineWrites)
