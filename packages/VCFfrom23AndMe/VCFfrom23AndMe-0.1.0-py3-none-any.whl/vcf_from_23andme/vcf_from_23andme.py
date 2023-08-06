def from_file(input, output, fasta, fai):
    """
    Args:
        input - A 23andme data file,
        output - Output VCF file,
        fasta - An uncompressed reference genome GRCh37 fasta file
        fai - The fasta index for for the reference

    """

    fai = __load_fai__(fai)
    snps = __load_23andme_data__(input)
    records = __get_vcf_records__(snps, fai, fasta)
    __write_vcf__(output, records)

def __load_fai__(fai):
    index = {}
    with open(fai) as f:
        for line in f:
            toks = line.split('\t')
            chrom = 'chr' + toks[0]
            if chrom == 'chrMT':
                chrom = 'chrM'
            length = int(toks[1])
            start = int(toks[2])
            linebases = int(toks[3])
            linewidth = int(toks[4])
            index[chrom] = (start, length, linebases, linewidth)
    return index

def __get_vcf_records__(pos_list, fai, fasta):
    with open(fasta) as f:
        def get_alts(ref, genotype):
            for x in genotype:
                assert x in 'ACGT'

            if len(genotype) == 1:
                if ref in genotype:
                    return []
                return [genotype]

            if ref == genotype[0] and ref == genotype[1]:
                return []
            if ref == genotype[0]:
                return [genotype[1]]
            if ref == genotype[1]:
                return [genotype[0]]
            return [genotype[0], genotype[1]]

        for (rsid, chrom, pos, genotype) in pos_list:
            start, _, linebases, linewidth = fai[chrom]
            n_lines = int(pos / linebases)
            n_bases = pos % linebases
            n_bytes = start + n_lines * linewidth + n_bases
            f.seek(n_bytes)
            ref = f.read(1)
            alts = get_alts(ref, genotype)
            pos = str(pos + 1)
            diploid = len(genotype) == 2
            assert ref not in alts
            assert len(alts) <= 2
            if diploid:
                if len(alts) == 2:
                    if alts[0] == alts[1]:
                        yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '1/1')
                    else:
                        yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '1/2')
                        yield (chrom, pos, rsid, ref, alts[1], '.', '.', '.', 'GT', '2/1')
                elif len(alts) == 1:
                    yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '0/1')
            elif len(alts) == 1:
                yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '1')

def __load_23andme_data__(input):
    with open(input) as f:
        for line in f:
            if line.startswith('#'): continue
            if line.strip():
                rsid, chrom, pos, genotype = line.strip().split('\t')
                if chrom == 'MT':
                    chrom = 'M'
                chrom = 'chr' + chrom
                if genotype != '--':
                    skip = False
                    for x in genotype:
                        if x not in 'ACTG':
                            skip = True
                    if not skip:
                        yield rsid, chrom, int(pos) - 1, genotype # subtract one because positions are 1-based indices

def __write_vcf_header__(f):
    f.write(
        """##fileformat=VCFv4.2
        ##source=23andme_to_vcf
        ##reference=GRCh37
        ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
        #CHROM POS ID REF ALT QUAL FILTER INFO FORMAT SAMPLE
        """)

def __write_vcf__(outfile, records):
    with open(outfile, 'w') as f:
        __write_vcf_header__(f)
        for record in records:
            f.write('\t'.join(record) + '\n')
