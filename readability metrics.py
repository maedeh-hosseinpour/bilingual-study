

import csv
import re
import textstat
from wordfreq import zipf_frequency


PASSAGES = {
    "p1_emperor": "Many years ago, an Emperor was so excessively fond of new clothes that he spent all his money on them. He did not trouble himself in the least about his soldiers, nor did he care to go to the theatre or the horse races, except if the occasions allowed him to show off his new clothes. He had a different suit for each hour of the day. Like any other king or emperor, one is accustomed to saying, 'He is sitting in council.' Instead, his advisors always said, 'The Emperor is sitting in his wardrobe.' Time passed away merrily in the large capital city. Strangers arrived every day at the fashionable king’s court. One day, two rogues, calling themselves weavers, made an appearance. \n\nThey mentioned that they knew how to weave fabrics with the most beautiful colors and elaborate patterns. They claimed that the clothes had the extraordinary property of remaining invisible to everyone who was unfit for the office he held or was exceedingly simple. 'These must indeed be splendid clothes!' thought the Emperor. 'Had I such a suit, I might, at once, find out which men in my realms are unfit for their office and I would also be able to distinguish the wise from the foolish! This fine fabric must be woven for me immediately.' And he ordered large sums of money to be given to both the weavers so they could begin their work immediately. So the two pretending weavers set up two looms and began to work very busily. In reality, they did nothing at all. They asked for the most delicate silk and the purest gold thread but put both into their own knapsacks, and then, they continued pretending to work at the empty looms until late at night.",
    "p2_evers":   "Born in 1925, Medgar Evers grew up under segregation in the deep South. He walked 12 miles daily to get to school, eventually earning his high school diploma. Evers served in the U.S. Army from 1943 to 1945, including as a sergeant at the Battle of Normandy. After the war, he attended and studied business at a historically black college now known as Alcorn State University, and he graduated in 1952 and moved to Mound Bayou, Mississippi, a town developed by African Americans. \n\nAs a military veteran who fought for his country, Evers expected that he would be able to vote. However, he and five friends were deterred at gunpoint. Racism denied his equal rights. Later, he organized boycotts of gas stations with the slogan “Don’t Buy Gas Where You Can’t Use the Restroom.” To fight state laws that made segregation legal, Evers applied to attend the University of Mississippi Law School, but his application was rejected because of his race. That same year, Evers was named the NAACP's first field secretary for Mississippi. In this position, he helped organize boycotts and set up new local chapters of the NAACP. He tried to desegregate public beaches, buses, and parks. Evers led voter registration drives, advocated for school integration, and led investigations into the murder of the teenager Emmett Till. \n\nEvers was a prominent black voice, and that made him a target. In the 1960s, civil rights activists lived under constant threat. In May 1963, a bomb was thrown into his garage, and then someone tried to hit him with a car. In June 1963, Evers returned home without his usual FBI or police escort. As he got out of his car, carrying a box of NAACP t-shirts that said “Jim Crow Must Go,” Medgar Evers was shot and killed. Mourned nationally, Evers was buried in Arlington National Cemetery, where he received full military honors.",
    "p3_russo":   "The Russo-Japanese War took place between the Empire of Japan and the Russian Empire between 1904 and 1905. The Japanese won the war in 1905, and the Russians lost. The war happened because the Russian Empire and the Empire of Japan disagreed over who should get parts of Manchuria and Korea. The war was fought mostly on the Liaodong Peninsula and Mukden, the seas around Korea, Japan, and the Yellow Sea. \n\nThe politics of both countries in the war were very complicated. Both wanted to gain land and economic benefits. The Chinese Empire of the Qing Dynasty was large but weak. As a result, Japan and Russia saw an opportunity. Both countries wanted and fought over Qing land and possessions. Russia wanted a warm-water port on the Pacific Ocean for its navy and trade. The harbor at Vladivostok freezes over in the winter, but Port Arthur could be used all year round. Russia had already rented the port from the Qing and had permission to build a Trans-Siberian railway from St Petersburg to Port Arthur. Japan wanted to expand its empire into Korea and China. Japan thought that when Russia completed its railway in 1906, it would be able to beat Japan in a war by being able to supply large numbers of troops there. \n\nThat obviously made the Japanese nervous, as tensions had been high. Japan wanted to compromise with Russia to avoid war, even if Russia got the better deal. Japan wanted more of Korea and China than it thought Russia would offer. Japan decided to attack before the railway was complete so that it could do well in a war against Russia. The war started with a Japanese surprise attack on Port Arthur and continued with Japanese victories in Manchuria and elsewhere. The last major battle was at Tsushima Strait, which destroyed the Russian Navy.",
    "p4_dolly":  "In 1984, British scientists cloned the first mammals by splitting a sheep embryo. At the time, no one thought it possible to clone an adult animal, but scientists at the Roslin Institute in Scotland persisted and succeeded. They used an adult sheep’s stem cell, found in bone marrow or mammary glands, and transferred the nucleus to another cell to create the embryo. On July 5, 1996, Dolly was born to a surrogate mother. The news of her birth thrilled the public and the scientific world. Although many people believe Dolly was the first clone, her birth was exciting because she was cloned from an adult sheep. \n\nThis opened up the field of stem cell research. Stem cells are our most basic cells that can develop into any other kind of cell, from muscle to brain cells. Scientists are studying how they can heal damaged tissue or organs, perhaps even helping paralyzed people walk again someday. Dolly’s birth, life, and death also brought ethical issues to the forefront. While stem cell research and cloning technology can and are certainly helping people, some debate whether it's a slippery slope toward radical human genetic engineering. The risks of designer babies or potentially deformed human clones are often mentioned, but the reality is that science is far from able to clone or even elect specific genetic traits. There is still much more to study before humanity is close to that possibility. \n\nDolly’s life was short; she died at six years old though sheep usually live for twice as long. What scientists realized is that specific proteins in her DNA called telomeres were much shorter than other sheep her age. Telomeres get shorter as we age, and Dolly’s were as short as her clone. This begged the question: when Dolly was born, was her DNA already the “same age” as her clone? Furthermore, what implications did that have for the future study of cloning?",
}


def lexical_metrics(text):
    """Word-frequency + diversity metrics (lower Zipf = rarer/harder words)."""

    words = re.findall(r"[A-Za-z']+", text.lower())
    n = len(words)
    if n == 0:
        return {}
    zipfs = [zipf_frequency(w, "en") for w in words]
    # share of words that are relatively rare (Zipf < 3.0 ~ outside common band)
    rare = sum(1 for z in zipfs if z < 3.0) / n
    types = len(set(words))
    return {
        "mean_word_freq_zipf": round(sum(zipfs) / n, 3),
        "pct_rare_words": round(100 * rare, 1),
        "type_token_ratio": round(types / n, 3),
    }


def metrics_for(text):
    row = {
        # ength / surface
        "words": textstat.lexicon_count(text, removepunct=True),
        "sentences": textstat.sentence_count(text),
        "mean_words_per_sentence": round(
            textstat.lexicon_count(text, removepunct=True)
            / max(textstat.sentence_count(text), 1), 2),
        "mean_syllables_per_word": round(
            textstat.syllable_count(text)
            / max(textstat.lexicon_count(text, removepunct=True), 1), 3),
        #readability formulas 
        "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 2),
        "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 2),
        "gunning_fog": round(textstat.gunning_fog(text), 2),
        "smog_index": round(textstat.smog_index(text), 2),
        "coleman_liau_index": round(textstat.coleman_liau_index(text), 2),
        "automated_readability_index": round(textstat.automated_readability_index(text), 2),
    }
    row.update(lexical_metrics(text))
    return row


def main():
    results = {pid: metrics_for(txt) for pid, txt in PASSAGES.items()}
    cols = list(next(iter(results.values())).keys())

    idw = max(len(p) for p in results)
    print(f"{'passage':<{idw}} | " + " | ".join(f"{c[:14]:>14}" for c in cols))
    print("-" * (idw + 3 + 17 * len(cols)))
    for pid, row in results.items():
        print(f"{pid:<{idw}} | " + " | ".join(f"{row[c]:>14}" for c in cols))


    with open("passage_metrics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["passage"] + cols)
        for pid, row in results.items():
            w.writerow([pid] + [row[c] for c in cols])
    


if __name__ == "__main__":
    main()