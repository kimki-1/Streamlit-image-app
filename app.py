import streamlit as st 
from PIL import Image, ImageFilter, ImageEnhance
import os 
from datetime import datetime

def load_image(image_file) :
    img = Image.open(image_file) 
    return img 

# 디렉토리와 이미지를 주면, 해당 디렉토리에 이미지를 저장하는 ㅏㅁ수 
def save_uploaded_file(directory, img) :

    if not os.path.exists(directory) :
        os.makedirs(directory)

    filename = 'company '+datetime.now().isoformat().replace(':','-').replace('.','-')

    img.save(directory+'/'+filename+'.jpg')

    return st.success('Saved file : {} in {}'.format( filename+'.jpg', directory ))

def main() :
    st.subheader('이미지파일 업로드')
    image_files_list = st.file_uploader('Uploader Image', type=['png', 'jpg', 'jpeg'], accept_multiple_files= True)
    # print(image_files_list)
    img_list = []
    if image_files_list is not None :
        # 2. 각 파일을 이미지로 바꿔줘야 한다.
        # 2-1.모든 파일이 img_list에 이미지로 저장됨
        for img_files in image_files_list :
            img = load_image(img_files)
            img_list.append(img)
            st.image(img)
                
        option_list = ['Show Image', 'Rotate Image', 'Create Thumbnail', 'Crop Image', 
        'Merge Images', 'Flip Image', 'Change Color', 'Filters - Sharpen', 
        'Filters - Edge Enhance', 'Contrast Image']
        option = st.selectbox('옵션을 선택하세요.', option_list)

        if option == 'Show Image' :
            for img in img_list :
                st.image(img)

            dir_name = st.text_input('파일 경로 입력')   
            if st.button('파일저장') :
                for img in img_list :
                    save_uploaded_file(dir_name, img )


        elif option == 'Rotate Image' :
            # 1. 유저가 입력
            rotate = st.slider('Rotate', 0, 360)
            # 2. 모든 이미지를 돌린다. 
            transformed_img_list = []
            for img in img_list :
                rotated_img = img.rotate(rotate)
                st.image(rotated_img)
                transformed_img_list.append(rotated_img)

            dir_name = st.text_input('파일 경로 입력')   
            if st.button('파일저장') :
                for img in transformed_img_list :
                    save_uploaded_file(dir_name, img )
                                  
        elif option == 'Create Thumbnail' :
            # 1. 이미지의 사이즈를 알아야 겠다.
            # print(img.size)
 
            # width_size = st.slider('너비 사이즈', 0, img.size[0])
            # higth_size = st.slider('높이 사이즈', 0, img.size[1])     
             

            transformed_img_list = []    
            for img in img_list :
                st.write(img.size) 
                width_size = st.number_input('너비 사이즈 입력', 1, img.size[0])
                higth_size = st.number_input('높이 사이즈 입력', 1, img.size[1])  
                size = (width_size, higth_size) 
                img.thumbnail( size )
                st.image(img)
                transformed_img_list.append(img)
        

            dir_name = st.text_input('파일 경로 입력')
            if st.button('파일저장') :
                for img in transformed_img_list :
                    save_uploaded_file(dir_name, img )

        elif option == 'Crop Image' :
            # 왼쪽 윗부분 부터시작해서, 너비와 깊이 만큼 잘라라 
            # 왼쪽 윗부분 좌표 (50, 100)
            # 너비 x축으로, 깊이 y축으로 계산한 종료좌표 (200, 200)
            # 시작 좌표 + (너비, 높이) => 크랍 종료 좌표 
            start_x = st.number_input('시작 x 좌표 입력 ', 0, img.size[0]-1)
            start_y = st.number_input('시작 y 좌표 입력', 0, img.size[1]-1)
            # ★★★ 예외 처리 한거 ★★★
            max_width = img.size[0] - start_x 
            max_higth = img.size[1] - start_y
            width = st.number_input('width 입력 ', 1, max_width)
            higth = st.number_input('higth 입력', 1, max_higth)
            
            box = (start_x, start_y, start_x + width, start_y + higth)
            st.write(box)
            cropped_img = img.crop(box)
            # cropped_img.save('data/crop.png')
            st.image(cropped_img)

        elif option == 'Merge Images' :
            merge_file = st.file_uploader('Uploader Image', type=['png', 'jpg', 'jpeg'], key= 'merge')

            if merge_file is not None :
                merge_img = load_image(merge_file)
            
                start_x = st.number_input('시작 x 좌표 입력 ', 0, img.size[0]-1)
                start_y = st.number_input('시작 y 좌표 입력', 0, img.size[1]-1)

                position = (start_x, start_y)
                img.paste(merge_img, position)
                st.image(img)



        elif option == 'Flip Image' :
            flip = st.radio('FlIP 선택 ', ['FLIP_LEFT_RIGHT', 'FLIP_TOP_BOTTOM'])
            transformed_img_list = []

            if flip == 'FLIP_LEFT_RIGHT' :
                for img in img_list :
                    flipped_img = img.transpose( Image.FLIP_LEFT_RIGHT )
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)

            elif flip == 'FLIP_TOP_BOTTOM' :
                for img in img_list :
                    flipped_img = img.transpose( Image.FLIP_TOP_BOTTOM)
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)

            dir_name = st.text_input('파일 경로 입력')
            if st.button('파일저장') :
                for img in transformed_img_list :
                    save_uploaded_file(dir_name, img )
    
        elif option == 'Change Color' : # change color 
            status = st.radio('색변경', ['Color', 'Gray', 'Black & White'])
            transformed_img_list = []

            if status == 'Color' :
                color = 'RGB' 
            elif status == 'Gray' :
                color = 'L'
            elif status == 'Black & White' :
                color = '1'
            for img in img_list :
                bw = img.convert(color)
                st.image(bw)
                transformed_img_list.append(bw)

            dir_name = st.text_input('파일 경로 입력')
            if st.button('파일저장') :
                for img in transformed_img_list :
                    save_uploaded_file(dir_name, img )

            ######################################################
            # bw_button = st.button('Black & White')
            # gray_button = st.button('Gray')
            # rgb_button = st.button('RGB')
            # # print(bw_button)
            # if bw_button == True :
            #     bw = img.convert('1') 
            #     # 1 = black & white , L = gray scale, RGB = 컬러로
            #     st.image(bw)
            # elif gray_button == True :
            #     gray = img.convert('L')
            #     st.image(gray)
            # elif rgb_button == True :
            #     rgb = img.convert('RGB')
            #     st.image(rgb)
            ######################################################

        elif option == 'Filters - Sharpen' : 
            for img in img_list :  
                sharp_img = img.filter(ImageFilter.SHARPEN)
                st.image(sharp_img)

        elif option == 'Filters - Edge Enhance' : # 선강조
            for img in img_list :
                edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
                st.image(edge_img)

        elif option == 'Contrast Image' : # 명암
            for img in img_list :
                contrast_img = ImageEnhance.Contrast(img).enhance(2)
                st.image(contrast_img)
            
        # 1. 이미지(한장)를 내가 마음대로 올릴 수 있어야 한다.
        # 2. 로테이트 이미지 누르면 각도를 선택할수 있게  나이하는걸로
        # 3. 썸네일 이미지 사이즈얻어와서 시작점을 주고 너비 높이 유저한테 받으면
        #    유저가 원하는 사이즈로 
        # 하드 코딩된 코드를, 유저한테 입력 받아서 처리할 수 있도록 바꾼다.
        # 4. 여러파일을 변환할 수 있도록 수정 
        #    각 옵션을 실행한뒤 저장하기 버튼을 누르면, 저장이 되도록
        #    저장 시에는, 디렉토리이름을 유저가 직접 입력하여 저장.

if __name__ == '__main__' :
    main()