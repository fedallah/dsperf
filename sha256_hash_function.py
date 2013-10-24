from hashlib import sha256
with open('testdata.csv', 'Ur', encoding='utf-8') as inputfile:
	for line in inputfile:
		hashme = sha256()
		hashme.update(line.encode(inputfile.encoding))
		line = line.split(',', 12)
		line.append(hashme.hexdigest())
		tuple(line)
		print(line)