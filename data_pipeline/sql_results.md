# SQL Query Results for Module 1 Data Pipeline

## Query: `q1_high_rated_in_stock`
```sql
SELECT title, price_gbp, rating 
            FROM books 
            WHERE rating >= 4 AND in_stock = 1;
```
**Output Table:**
```text
                                                                        title  price_gbp  rating
             Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond      49.43       4
                                             A Year in Provence (Provence #1)      56.88       4
                                           1,000 Places to See Before You Die      26.08       5
                                                                Sharp Objects      47.82       4
                                                          The Past Never Ends      56.50       4
                              The Murder of Roger Ackroyd (Hercule Poirot #4)      44.10       4
                                       A Time of Torment (Charlie Parker #14)      48.35       5
                        Murder at the 42nd Street Library (Raymond Ambler #1)      54.36       4
            What Happened on Beale Street (Secrets of the South Mysteries #2)      25.37       5
     The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)      52.30       5
                             Delivering the Truth (Quaker Midwife Mystery #1)      20.89       4
                          The Mysterious Affair at Styles (Hercule Poirot #1)      24.80       4
                                            The Silkworm (Cormoran Strike #2)      23.05       5
       The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70       4
                                                            The Girl You Lost      12.29       5
                                                            The Secret Garden      15.08       4
                                               Little Women (Little Women #1)      28.07       4
The Complete Stories and Poems (The Works of Edgar Allan Poe [Cameo Edition])      26.78       4
                                                    The Story of Hong Gildong      43.19       4
                                      A Flight of Arrows (The Pathfinders #2)      55.53       5
                                                                 Mrs. Houdini      30.25       5
                                                    The Marriage of Opposites      28.08       4
                                                            A Paris Apartment      39.01       4
                              World Without End (The Pillars of the Earth #2)      32.97       4
                                                        The Passion of Dolssa      28.32       5
                                                       Voyager (Outlander #3)      21.07       5
                                                                 The Red Tent      35.66       5
                                                       Between Shades of Gray      20.79       5
                                                          While You Were Mine      41.32       5
                                                        Lost Among the Living      27.70       4
                            A Spy's Devotion (The Regency Spies of London #1)      16.97       5
```

## Query: `q2_top_expensive`
```sql
SELECT title, price_gbp 
            FROM books 
            ORDER BY price_gbp DESC 
            LIMIT 10;
```
**Output Table:**
```text
                                                                 title  price_gbp
                                         Boar Island (Anna Pigeon #19)      59.48
                                                               Candide      58.63
The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70
                                                           Animal Farm      57.22
                                      A Year in Provence (Provence #1)      56.88
                                                   The Past Never Ends      56.50
                                      The Last Painting of Sara de Vos      55.55
             Alice in Wonderland (Alice's Adventures in Wonderland #1)      55.53
                               A Flight of Arrows (The Pathfinders #2)      55.53
                 Murder at the 42nd Street Library (Raymond Ambler #1)      54.36
```

## Query: `q3_distinct_ratings`
```sql
SELECT DISTINCT rating 
            FROM books 
            ORDER BY rating DESC;
```
**Output Table:**
```text
 rating
      5
      4
      3
      2
      1
```

## Query: `q4_price_between`
```sql
SELECT title, price_gbp 
            FROM books 
            WHERE price_gbp BETWEEN 20 AND 40;
```
**Output Table:**
```text
                                                                                            title  price_gbp
                              Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel      36.94
                                                                             Under the Tuscan Sun      37.33
                                                                         The Great Railway Bazaar      30.54
The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)      23.21
                                                        Neither Here nor There: Travels in Europe      38.95
                                                               1,000 Places to See Before You Die      26.08
                                                                 Poisonous (Max Revere Novels #3)      26.80
                                                                                      Most Wanted      35.28
                                                                                        The Widow      27.26
                                What Happened on Beale Street (Secrets of the South Mysteries #2)      25.37
                                                 Delivering the Truth (Quaker Midwife Mystery #1)      20.89
                                              The Mysterious Affair at Styles (Hercule Poirot #1)      24.80
                                                            In the Woods (Dublin Murder Squad #1)      38.38
                                                                The Silkworm (Cormoran Strike #2)      23.05
                                                               Extreme Prey (Lucas Davenport #26)      25.40
                                                              Career of Evil (Cormoran Strike #3)      24.72
                                                             Blood Defense (Samantha Brinkman #1)      20.30
                                                                                The Metamorphosis      28.58
                                                                   Little Women (Little Women #1)      28.07
                                                                               Gone with the Wind      32.49
                                                                       The Picture of Dorian Gray      29.70
                    The Complete Stories and Poems (The Works of Edgar Allan Poe [Cameo Edition])      26.78
                                                                                          Beowulf      38.35
                                                                         And Then There Were None      35.01
                                                                            Sense and Sensibility      37.46
                                                                                             Emma      32.93
                        Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton      29.69
                                                                            The House by the Lake      36.95
                                                                                     Mrs. Houdini      30.25
                                                                        The Marriage of Opposites      28.08
                                                                             Love, Lies and Spies      20.55
                                                                                A Paris Apartment      39.01
                                                                           The Invention of Wings      37.34
                                                  World Without End (The Pillars of the Earth #2)      32.97
                                                                            The Passion of Dolssa      28.32
                                                                        Girl With a Pearl Earring      26.77
                                                                           Voyager (Outlander #3)      21.07
                                                                                     The Red Tent      35.66
                                                                           Between Shades of Gray      20.79
                                                                                The Secret Healer      34.56
                                                                                         Starlark      25.83
                                                                            Lost Among the Living      27.70
```

## Query: `q5_category_join`
```sql
SELECT b.title, c.category_name, b.price_inr 
            FROM books b 
            JOIN categories c ON b.category_id = c.category_id 
            WHERE c.category_name IN ('Travel', 'Mystery');
```
**Output Table:**
```text
                                                                                            title category_name  price_inr
                                                                                    Sharp Objects       Mystery    5045.01
                                                                             In a Dark, Dark Wood       Mystery    2070.96
                                                                              The Past Never Ends       Mystery    5960.75
                                                                                 A Murder in Time       Mystery    1755.52
                                                  The Murder of Roger Ackroyd (Hercule Poirot #4)       Mystery    4652.55
                                                                   The Last Mile (Amos Decker #2)       Mystery    5719.16
                                                           That Darkness (Gardiner and Renner #1)       Mystery    1468.56
                                                             Tastes Like Fear (DI Marnie Rome #3)       Mystery    1127.79
                                                           A Time of Torment (Charlie Parker #14)       Mystery    5100.92
                                                          A Study in Scarlet (Sherlock Holmes #1)       Mystery    1765.02
                                                                 Poisonous (Max Revere Novels #3)       Mystery    2827.40
                                            Murder at the 42nd Street Library (Raymond Ambler #1)       Mystery    5734.98
                                                                                      Most Wanted       Mystery    3722.04
                                                                       Hide Away (Eve Duncan #20)       Mystery    1249.12
                                                                    Boar Island (Anna Pigeon #19)       Mystery    6275.14
                                                                                        The Widow       Mystery    2875.93
                                                                                Playing with Fire       Mystery    1446.41
                                What Happened on Beale Street (Secrets of the South Mysteries #2)       Mystery    2676.54
                         The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)       Mystery    5517.65
                                                 Delivering the Truth (Quaker Midwife Mystery #1)       Mystery    2203.90
                                              The Mysterious Affair at Styles (Hercule Poirot #1)       Mystery    2616.40
                                                            In the Woods (Dublin Murder Squad #1)       Mystery    4049.09
                                                                The Silkworm (Cormoran Strike #2)       Mystery    2431.78
                                                                                       The Exiled       Mystery    4583.98
                                                        The Cuckoo's Calling (Cormoran Strike #1)       Mystery    2026.66
                                                               Extreme Prey (Lucas Davenport #26)       Mystery    2679.70
                                                              Career of Evil (Cormoran Strike #3)       Mystery    2607.96
                           The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)       Mystery    6087.35
                                                                                The Girl You Lost       Mystery    1296.59
                                                        The Girl In The Ice (DCI Erika Foster #1)       Mystery    1672.18
                                                             Blood Defense (Samantha Brinkman #1)       Mystery    2141.65
                                                              1st to Die (Women's Murder Club #1)       Mystery    5694.89
                                                                          It's Only the Himalayas        Travel    4765.44
                                 Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond        Travel    5214.86
                               See America: A Celebration of Our National Parks & Treasured Sites        Travel    5155.78
                              Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel        Travel    3897.17
                                                                             Under the Tuscan Sun        Travel    3938.31
                                                                               A Summer In Europe        Travel    4677.87
                                                                         The Great Railway Bazaar        Travel    3221.97
                                                                 A Year in Provence (Provence #1)        Travel    6000.84
The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)        Travel    2448.66
                                                        Neither Here nor There: Travels in Europe        Travel    4109.23
                                                               1,000 Places to See Before You Die        Travel    2751.44
```

