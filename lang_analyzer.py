import json
import traceback
import langid
import matplotlib.pyplot as plt
import pandas as pd

lang_name = {"ab":"Abkhazian", "aa":"Afar", "af":"Afrikaans", "ak":"Akan", "sq":"Albanian", "am":"Amharic", "ar":"Arabic", "an":"Aragonese", "hy":"Armenian", "as":"Assamese", "av":"Avaric", "ae":"Avestan", "ay":"Aymara", "az":"Azerbaijani", "bm":"Bambara", "ba":"Bashkir", "eu":"Basque", "be":"Belarusian", "bn":"Bengali", "bh":"Bihari languages", "bi":"Bislama", "bs":"Bosnian", "br":"Breton", "bg":"Bulgarian", "my":"Burmese", "ca":"Catalan", "ch":"Chamorro", "ce":"Chechen", "ny":"Chichewa, Chewa, Nyanja", "zh":"Chinese", "cv":"Chuvash", "kw":"Cornish", "co":"Corsican", "cr":"Cree", "hr":"Croatian", "cs":"Czech", "da":"Danish", "dv":"Maldivian", "nl":"Dutch", "dz":"Dzongkha", "en":"English", "eo":"Esperanto", "et":"Estonian", "ee":"Ewe", "fo":"Faroese", "fj":"Fijian", "fi":"Finnish", "fr":"French", "ff":"Fulah", "gl":"Galician", "ka":"Georgian", "de":"German", "el":"Greek", "gn":"Guarani", "gu":"Gujarati", "ht":"Haitian", "ha":"Hausa", "he":"Hebrew", "hz":"Herero", "hi":"Hindi", "ho":"Hiri Motu", "hu":"Hungarian", "ia":"Interlingua (International Auxiliary Language Association)", "in":"Indonesian", "id":"Indonesian", "ie":"Interlingue, Occidental", "ga":"Irish", "ig":"Igbo", "ik":"Inupiaq", "io":"Ido", "is":"Icelandic", "it":"Italian", "iu":"Inuktitut", "ja":"Japanese", "jv":"Javanese", "kl":"Kalaallisut, Greenlandic", "kn":"Kannada", "kr":"Kanuri", "ks":"Kashmiri", "kk":"Kazakh", "km":"Khmer", "ki":"Kikuyu, Gikuyu", "rw":"Kinyarwanda", "ky":"Kirghiz, Kyrgyz", "kv":"Komi", "kg":"Kongo", "ko":"Korean", "ku":"Kurdish", "kj":"Kuanyama, Kwanyama", "la":"Latin", "lb":"Luxembourgish, Letzeburgesch", "lg":"Ganda", "li":"Limburgan, Limburger, Limburgish", "ln":"Lingala", "lo":"Lao", "lt":"Lithuanian", "lu":"Luba-Katanga", "lv":"Latvian", "gv":"Manx", "mk":"Macedonian", "mg":"Malagasy", "ms":"Malay", "ml":"Malayalam", "mt":"Maltese", "mi":"Maori", "mr":"Marathi", "mh":"Marshallese", "mn":"Mongolian", "na":"Nauru", "nv":"Navajo, Navaho", "nd":"North Ndebele", "ne":"Nepali", "ng":"Ndonga", "nb":"Norwegian Bokmål", "nn":"Norwegian Nynorsk", "no":"Norwegian", "ii":"Sichuan Yi, Nuosu", "nr":"South Ndebele", "oc":"Occitan", "oj":"Ojibwa", "cu":"Church Slavic, Old Slavonic, Church Slavonic, Old Bulgarian, Old Church Slavonic", "om":"Oromo", "or":"Oriya", "os":"Ossetian, Ossetic", "pa":"Panjabi", "pi":"Pali", "fa":"Persian", "pl":"Polish", "ps":"Pashto", "pt":"Portuguese", "qu":"Quechua", "rm":"Romansh", "rn":"Rundi", "ro":"Romanian", "ru":"Russian", "sa":"Sanskrit", "sc":"Sardinian", "sd":"Sindhi", "se":"Northern Sami", "sm":"Samoan", "sg":"Sango", "sr":"Serbian", "gd":"Gaelic, Scottish Gaelic", "sn":"Shona", "si":"Sinhala", "sk":"Slovak", "sl":"Slovenian", "so":"Somali", "st":"Southern Sotho", "es":"Spanish", "su":"Sundanese", "sw":"Swahili", "ss":"Swati", "sv":"Swedish", "ta":"Tamil", "te":"Telugu", "tg":"Tajik", "th":"Thai", "ti":"Tigrinya", "bo":"Tibetan", "tk":"Turkmen", "tl":"Tagalog", "tn":"Tswana", "to":"Tonga (Tonga Islands)", "tr":"Turkish", "ts":"Tsonga", "tt":"Tatar", "tw":"Twi", "ty":"Tahitian", "ug":"Uyghur", "uk":"Ukrainian", "ur":"Urdu", "uz":"Uzbek", "ve":"Venda", "vi":"Vietnamese", "vo":"Volapük", "wa":"Walloon", "cy":"Welsh", "wo":"Wolof", "fy":"Western Frisian", "xh":"Xhosa", "yi":"Yiddish", "yo":"Yoruba", "za":"Zhuang, Chuang", "zu":"Zulu", "iw":"Hebrew", "und":"Undefined", "fil":"Filipino", "msa":"Malay", "zh-cn":"Chinese (Simplified)", "zh-tw":"Chinese (Traditional)", "ckb":"Sorani Kurdish", "others":"Others"}

code_country = {"AF":"Afghanistan", "AX":"Ã…land Islands", "AL":"Albania", "DZ":"Algeria", "AS":"American Samoa", "AD":"Andorra", "AO":"Angola", "AI":"Anguilla", "AQ":"Antarctica", "AG":"Antigua and Barbuda", "AR":"Argentina", "AM":"Armenia", "AW":"Aruba", "AU":"Australia", "AT":"Austria", "AZ":"Azerbaijan", "BS":"Bahamas", "BH":"Bahrain", "BD":"Bangladesh", "BB":"Barbados", "BY":"Belarus", "BE":"Belgium", "BZ":"Belize", "BJ":"Benin", "BM":"Bermuda", "BT":"Bhutan", "BO":"Bolivia, Plurinational State of", "BQ":"Bonaire, Sint Eustatius and Saba", "BA":"Bosnia and Herzegovina", "BW":"Botswana", "BV":"Bouvet Island", "BR":"Brazil", "IO":"British Indian Ocean Territory", "BN":"Brunei Darussalam", "BG":"Bulgaria", "BF":"Burkina Faso", "BI":"Burundi", "KH":"Cambodia", "CM":"Cameroon", "CA":"Canada", "CV":"Cape Verde", "KY":"Cayman Islands", "CF":"Central African Republic", "TD":"Chad", "CL":"Chile", "CN":"China", "CX":"Christmas Island", "CC":"Cocos (Keeling) Islands", "CO":"Colombia", "KM":"Comoros", "CG":"Congo", "CD":"Congo, the Democratic Republic of the", "CK":"Cook Islands", "CR":"Costa Rica", "CI":"CÃ´te d'Ivoire", "HR":"Croatia", "CU":"Cuba", "CW":"CuraÃ§ao", "CY":"Cyprus", "CZ":"Czech Republic", "DK":"Denmark", "DJ":"Djibouti", "DM":"Dominica", "DO":"Dominican Republic", "EC":"Ecuador", "EG":"Egypt", "SV":"El Salvador", "GQ":"Equatorial Guinea", "ER":"Eritrea", "EE":"Estonia", "ET":"Ethiopia", "FK":"Falkland Islands (Malvinas)", "FO":"Faroe Islands", "FJ":"Fiji", "FI":"Finland", "FR":"France", "GF":"French Guiana", "PF":"French Polynesia", "TF":"French Southern Territories", "GA":"Gabon", "GM":"Gambia", "GE":"Georgia", "DE":"Germany", "GH":"Ghana", "GI":"Gibraltar", "GR":"Greece", "GL":"Greenland", "GD":"Grenada", "GP":"Guadeloupe", "GU":"Guam", "GT":"Guatemala", "GG":"Guernsey", "GN":"Guinea", "GW":"Guinea-Bissau", "GY":"Guyana", "HT":"Haiti", "HM":"Heard Island and McDonald Islands", "VA":"Holy See (Vatican City State)", "HN":"Honduras", "HK":"Hong Kong", "HU":"Hungary", "IS":"Iceland", "IN":"India", "ID":"Indonesia", "IR":"Iran, Islamic Republic of", "IQ":"Iraq", "IE":"Ireland", "IM":"Isle of Man", "IL":"Israel", "IT":"Italy", "JM":"Jamaica", "JP":"Japan", "JE":"Jersey", "JO":"Jordan", "KZ":"Kazakhstan", "KE":"Kenya", "KI":"Kiribati", "KP":"Korea, Democratic People's Republic of", "KR":"Korea, Republic of", "KW":"Kuwait", "KG":"Kyrgyzstan", "LA":"Lao People's Democratic Republic", "LV":"Latvia", "LB":"Lebanon", "LS":"Lesotho", "LR":"Liberia", "LY":"Libya", "LI":"Liechtenstein", "LT":"Lithuania", "LU":"Luxembourg", "MO":"Macao", "MK":"Macedonia, the Former Yugoslav Republic of", "MG":"Madagascar", "MW":"Malawi", "MY":"Malaysia", "MV":"Maldives", "ML":"Mali", "MT":"Malta", "MH":"Marshall Islands", "MQ":"Martinique", "MR":"Mauritania", "MU":"Mauritius", "YT":"Mayotte", "MX":"Mexico", "FM":"Micronesia, Federated States of", "MD":"Moldova, Republic of", "MC":"Monaco", "MN":"Mongolia", "ME":"Montenegro", "MS":"Montserrat", "MA":"Morocco", "MZ":"Mozambique", "MM":"Myanmar", "NA":"Namibia", "NR":"Nauru", "NP":"Nepal", "NL":"Netherlands", "NC":"New Caledonia", "NZ":"New Zealand", "NI":"Nicaragua", "NE":"Niger", "NG":"Nigeria", "NU":"Niue", "NF":"Norfolk Island", "MP":"Northern Mariana Islands", "NO":"Norway", "OM":"Oman", "PK":"Pakistan", "PW":"Palau", "PS":"Palestine, State of", "PA":"Panama", "PG":"Papua New Guinea", "PY":"Paraguay", "PE":"Peru", "PH":"Philippines", "PN":"Pitcairn", "PL":"Poland", "PT":"Portugal", "PR":"Puerto Rico", "QA":"Qatar", "RE":"RÃ©union", "RO":"Romania", "RU":"Russian Federation", "RW":"Rwanda", "BL":"Saint BarthÃ©lemy", "SH":"Saint Helena, Ascension and Tristan da Cunha", "KN":"Saint Kitts and Nevis", "LC":"Saint Lucia", "MF":"Saint Martin (French part)", "PM":"Saint Pierre and Miquelon", "VC":"Saint Vincent and the Grenadines", "WS":"Samoa", "SM":"San Marino", "ST":"Sao Tome and Principe", "SA":"Saudi Arabia", "SN":"Senegal", "RS":"Serbia", "SC":"Seychelles", "SL":"Sierra Leone", "SG":"Singapore", "SX":"Sint Maarten (Dutch part)", "SK":"Slovakia", "SI":"Slovenia", "SB":"Solomon Islands", "SO":"Somalia", "ZA":"South Africa", "GS":"South Georgia and the South Sandwich Islands", "SS":"South Sudan", "ES":"Spain", "LK":"Sri Lanka", "SD":"Sudan", "SR":"Suriname", "SJ":"Svalbard and Jan Mayen", "SZ":"Swaziland", "SE":"Sweden", "CH":"Switzerland", "SY":"Syrian Arab Republic", "TW":"Taiwan, Province of China", "TJ":"Tajikistan", "TZ":"Tanzania, United Republic of", "TH":"Thailand", "TL":"Timor-Leste", "TG":"Togo", "TK":"Tokelau", "TO":"Tonga", "TT":"Trinidad and Tobago", "TN":"Tunisia", "TR":"Turkey", "TM":"Turkmenistan", "TC":"Turks and Caicos Islands", "TV":"Tuvalu", "UG":"Uganda", "UA":"Ukraine", "AE":"United Arab Emirates", "GB":"United Kingdom", "US":"United States", "UM":"United States Minor Outlying Islands", "UY":"Uruguay", "UZ":"Uzbekistan", "VU":"Vanuatu", "VE":"Venezuela, Bolivarian Republic of", "VN":"Viet Nam", "VG":"Virgin Islands, British", "VI":"Virgin Islands, U.S.", "WF":"Wallis and Futuna", "EH":"Western Sahara", "YE":"Yemen", "ZM":"Zambia", "ZW":"Zimbabwe"}


def analyze_tweets(tweet_file):
    count = 0
    us_tweet_count = 0
    lang = dict()
    us_lang = dict()
    countries = dict()
    geo_tag_count = 0
    coord_count = 0
    us_coord_count = 0
    langid_clsfr = dict()
    disagree_count = 0
    disagree_dict = dict()
    cnt_lng = dict()
    with open(tweet_file, 'r') as fin:
        for line in fin:
            try:
                tweet = json.loads(line.strip())
                if 'text' in tweet:
                    lang_id = tweet['lang']
                    lang[lang_id] = lang.get(lang_id, 0) + 1
                    count += 1
                    if tweet['place']:
                        geo_tag_count += 1
                        if tweet['coordinates']:
                            coord_count += 1
                        if 'country_code' in tweet['place'] and len(tweet['place']['country_code']):
                            country_name = tweet['place']['country_code']
                            countries[country_name] = countries.get(country_name, 0) + 1
                            if country_name in cnt_lng:
                                cnt_lng[country_name][lang_id] = cnt_lng[country_name].get(lang_id, 0) + 1
                            else:
                                cnt_lng[country_name] = dict()
                                cnt_lng[country_name][lang_id] = cnt_lng[country_name].get(lang_id, 0) + 1
                            if tweet['place']['country_code'] == 'US':
                                us_lang[lang_id] = us_lang.get(lang_id, 0) + 1
                                us_tweet_count += 1
                                if tweet['coordinates']:
                                    us_coord_count += 1

                    language, _ = langid.classify(tweet['text'])
                    langid_clsfr[language] = langid_clsfr.get(language, 0) + 1
                    if lang_id != language and not (lang_id == 'in' and language == 'id'):
                        disagree_count += 1
                        disagree_dict[(lang_id, language)] = disagree_dict.get((lang_id, language), 0) + 1

            except Exception as e:
                print(traceback.format_exc())

    print('Total tweet count: ' + str(count))
    print('Total tweet count that are language tagged: ' + str(count - lang['und']) + ' and percentage(%): ' + str((count - lang['und'])*100/count))
    print('Total Tweeter-API tagged language count: ' + str(len(lang.keys())))

    print('\n\nDistribution of language in tweets:')
    print('{:>38}'.format('Language (code)') + ' ' + '{:>6}'.format('Count') + '  ' + '{:>10}'.format('Percent(%)'))
    for i, id in enumerate(sorted(lang, key=lang.get, reverse=True)):
        print('{:>2d}'.format(i+1) + '{:.>36}'.format(lang_name[id] + ' (' + id + ')') + ' ' + '{:>6d}'.format(lang[id]) + '  ' + '{:>10.2f}'.format(lang[id]*100/count))

    print('\n\nTotal count of langId tagged languages: ' + str(len(langid_clsfr.keys())))
    print('Total agreed tweet language by Tweeter API and LangID: ' + str(count - disagree_count) + ' and percentage(%): ' + str((count - disagree_count) * 100 / count))
    print('Total disagreed tweet language by LangID: ' + str(disagree_count) + ' and percentage(%): ' + str(disagree_count*100/count))

    print('\nKind of languages Tweeter and LangId disagreed:')
    print('{:>38}'.format('Twitter lang tag (code)') + '\t'+ '{:<36}'.format('LangID tag (code)') + ' ' + '{:>6}'.format('Count') + '  ' + '{:>10}'.format('Percent(%)'))
    for i, tuple in enumerate(sorted(disagree_dict, key=disagree_dict.get, reverse=True)):
        print('{:>2d}'.format(i+1) + '{:.>36}'.format(lang_name[tuple[0]] + ' (' + tuple[0] + ')') + '\t' + '{:.<36}'.format(lang_name[tuple[1]] + ' (' + tuple[1] + ')') + ' ' + '{:>6d}'.format(disagree_dict[tuple]) + '  ' + '{:>10.2f}'.format(disagree_dict[tuple]*100/disagree_count))

    print('\n\nTotal country count: ' + str(len(countries.keys())))
    print('Total geo-tagged(place-tagged) tweet count: ' + str(geo_tag_count) + ' and percentage(%): ' + str(geo_tag_count*100/count))
    print('Total coordinate-tagged tweet count: ' + str(coord_count) + ' and percentage(%): ' + str(coord_count*100/count))

    print('\nTwitter distribution among countries:')
    print('{:>39}'.format('Country (code)') + ' ' + '{:>6}'.format('Count') + '  ' + '{:>10}'.format('Percent(%)'))
    for i, country in enumerate(sorted(countries, key=countries.get, reverse=True)):
        print('{:>2d}'.format(i + 1) + '{:.>37}'.format(code_country[country] + ' (' + country + ')') + ' ' + '{:>6d}'.format(countries[country]) + '  ' + '{:>10.2f}'.format(countries[country] * 100 / geo_tag_count))

    print('\n\nTotal US tweet: ' + str(us_tweet_count))
    print('Total US tweet count with coordinate tag: ' + str(us_coord_count) + ' and percentage(%): ' + str(us_coord_count*100/us_tweet_count))

    print('\nLanguage distribution in US tweets:')
    print('{:>38}'.format('US Language (code)') + ' ' + '{:>6}'.format('Count') + '  ' + '{:>10}'.format('Percent(%)'))
    for i, id in enumerate(sorted(us_lang, key=us_lang.get, reverse=True)):
        print('{:>2d}'.format(i + 1) + '{:.>36}'.format(lang_name[id] + ' (' + id + ')') + ' ' + '{:>6d}'.format(
            us_lang[id]) + '  ' + '{:>10.2f}'.format(us_lang[id] * 100 / us_tweet_count))

    print("\n\nFigure 1 shows the distribution of Tweet language")
    print("\nFigure 2 shows language share of the most active countries\n")

    sizes = []
    top_ten_labels = []
    for i, id in enumerate(sorted(lang, key=lang.get, reverse=True)):
        if i == 10:
            top_ten_labels.append('Others')
            sizes.append(100-sum(sizes))
            break
        else:
            top_ten_labels.append(lang_name[id])
            sizes.append(lang[id]*100/count)

    explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=top_ten_labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title("Figure 1: Distribution of Tweet language", y=-0.05)
    plt.show()

    lngs = ['en', 'pt', 'ja', 'es', 'tl', 'in', 'it', 'ko', 'ar', 'fr', 'tr', 'others']
    raw_data = dict()
    for lng in lngs:
        raw_data[lng] = []
        for i, cnt in enumerate(sorted(countries, key=countries.get, reverse=True)[:8]):
            if lng != 'others':
                raw_data[lng].append(cnt_lng[cnt].get(lng, 0))
            else:
                others = 0
                for ln in lngs[:11]:
                    others += raw_data[ln][i]
                raw_data[lng].append(countries[cnt] - others)

    df = pd.DataFrame(raw_data)
    totals = [a+b+c+d+e+f+g+h+i+j+k+l for a, b, c, d, e, f, g, h, i, j, k, l in zip(df['en'], df['pt'], df['ja'], df['es'], df['tl'], df['in'], df['it'], df['ko'], df['ar'], df['fr'], df['tr'], df['others'])]
    lng_bars = []
    for lng in lngs:
        lng_bars.append([i/j * 100 for i, j in zip(df[lng], totals)])

    barWidth = 0.3
    cnts = []
    r = [0, 1, 2, 3, 4, 5, 6, 7]
    for cnt in sorted(countries, key=countries.get, reverse=True)[:8]:
        cnts.append(code_country[cnt])

    plt.bar(r, lng_bars[0], color='#b5ffb9', edgecolor='white', width=barWidth, label=lang_name[lngs[0]])
    plt.bar(r, lng_bars[1], bottom=lng_bars[0], color='#f9bc86', edgecolor='white', width=barWidth, label=lang_name[lngs[1]])
    plt.bar(r, lng_bars[2], bottom=[i+j for i, j in zip(lng_bars[0], lng_bars[1])], color='#a3acff', edgecolor='white', width=barWidth, label=lang_name[lngs[2]])
    plt.bar(r, lng_bars[3], bottom=[i+j+k for i, j, k in zip(lng_bars[0], lng_bars[1], lng_bars[2])], color='#566573', edgecolor='white', width=barWidth, label=lang_name[lngs[3]])
    plt.bar(r, lng_bars[4], bottom=[i+j+k+l for i, j, k, l in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3])], color='#4A235A', edgecolor='white', width=barWidth, label=lang_name[lngs[4]])
    plt.bar(r, lng_bars[5], bottom=[i+j+k+l+m for i, j, k, l, m in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3], lng_bars[4])], color='#F4D03F', edgecolor='white', width=barWidth, label=lang_name[lngs[5]])
    plt.bar(r, lng_bars[6], bottom=[i+j+k+l+m+n for i, j, k, l, m, n in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3], lng_bars[4], lng_bars[5])], color='#AAB7B8', edgecolor='white', width=barWidth, label=lang_name[lngs[6]])
    plt.bar(r, lng_bars[7], bottom=[i+j+k+l+m+n+o for i, j, k, l, m, n, o in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3], lng_bars[4], lng_bars[5], lng_bars[6])], color='#73C6B6', edgecolor='white', width=barWidth, label=lang_name[lngs[7]])
    plt.bar(r, lng_bars[8], bottom=[i+j+k+l+m+n+o+p for i, j, k, l, m, n, o, p in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3], lng_bars[4], lng_bars[5], lng_bars[6], lng_bars[7])], color='#F986C3', edgecolor='white', width=barWidth, label=lang_name[lngs[8]])
    plt.bar(r, lng_bars[9], bottom=[i+j+k+l+m+n+o+p+q for i, j, k, l, m, n, o, p, q in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3], lng_bars[4], lng_bars[5], lng_bars[6], lng_bars[7], lng_bars[8])], color='#E74C3C', edgecolor='white', width=barWidth, label=lang_name[lngs[9]])
    plt.bar(r, lng_bars[10], bottom=[i+j+k+l+m+n+o+p+q+r for i, j, k, l, m, n, o, p, q, r in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3], lng_bars[4], lng_bars[5], lng_bars[6], lng_bars[7], lng_bars[8], lng_bars[9])], color='#5DADE2', edgecolor='white', width=barWidth, label=lang_name[lngs[10]])
    plt.bar(r, lng_bars[11], bottom=[i+j+k+l+m+n+o+p+q+r+s for i, j, k, l, m, n, o, p, q, r, s in zip(lng_bars[0], lng_bars[1], lng_bars[2], lng_bars[3], lng_bars[4], lng_bars[5], lng_bars[6], lng_bars[7], lng_bars[8], lng_bars[9], lng_bars[10])], color='#784212', edgecolor='white', width=barWidth, label=lang_name[lngs[11]])

    plt.xticks(r, cnts)
    plt.xlabel("Country")
    plt.ylabel("Tweet Language Percentage (%)")
    plt.title("Figure 2: Language share of the most active countries", y=-0.25)
    plt.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=4)
    plt.show()


if __name__ == '__main__':
    analyze_tweets('tweets.txt')
