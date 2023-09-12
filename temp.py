import pandas as pd


if __name__ == '__main__':
    # ipoh = pd.read_excel("Extra\IpohData.xlsx")
    # ipoh['Location'] = 'Ipoh'
    # kinabalu = pd.read_excel("Extra\KinabaluData.xlsx")
    # kinabalu['Location'] = 'Kinabalu'
    # melaka = pd.read_excel("Extra\MelakaData.xlsx")
    # melaka['Location'] = 'Melaka'

    # extradet1 = pd.read_excel("Extra\ExtraDetail1.xlsx")
    # extradet2 = pd.read_excel("Extra\ExtraDetail2.xlsx")
    # extradet3 = pd.read_excel("Extra\ExtraDetail3.xlsx")
    # extra = pd.concat([extradet1,extradet2,extradet3], ignore_index = True)
    # extra.to_excel("Extra\ExtraDetail.xlsx", index=False)

    # extradata = pd.read_excel("Extra\ExtraData.xlsx")
    # extradetail = pd.read_excel("Extra\ExtraDetail.xlsx")
    # DataAndDetail = pd.concat([extradata, extradetail], axis=1)
    # DataAndDetail.to_excel("Extra\DataAndDetail.xlsx", index=False)

    # dad = pd.read_excel("Extra\DataAndDetail.xlsx")
    # review = pd.read_excel("Extra\ExtraReview.xlsx")
    # ExtraFinal = pd.concat([dad, review], axis=1)
    # ExtraFinal.to_excel("Extra\ExtraFinal.xlsx", index=False)
    rest = pd.read_excel("RestaurantFinal.xlsx")
    print(rest['Review'][0])

