# Model
class MainPageAdItem(models.Model):
    ad_bg_baner = models.ImageField(upload_to='media/mainpageaditem/bg_baner', verbose_name='عکس بک گراند تبلیغاتی')
    ad_baner = models.ImageField(upload_to='media/mainpageaditem/baner', verbose_name='عکس تبلیغاتی')
    content_type = models.ForeignKey(c_model.ContentType, on_delete=models.CASCADE, verbose_name='سینمایی / سریال')
    object_id = models.PositiveIntegerField(verbose_name='ای دی سینمایی / سریال')
    media_object = fields.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'سینمایی / سریال تبلیغاتی بالای صفحه اصلی'
        verbose_name_plural = 'سینمایی / سریال های تبلیغاتی بالای صفحه اصلی'


# Views
all_ad = MainPageAdItem.objects.prefetch_related('media_object').select_related('content_type').all()[:10]
data = serializers.serialize('json', all_ad)


# Context

'all_media': all_ad,
'dict_media': all_ad.values(),


# Admin

class MainPageAdItemInline(admin.TabularInline):
    model = MainPageAdItem
    extra = 5


@admin.register(MainPageAdItem)
class MainPageAdItemAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id']



# HTML: home.html

        var medias = [
                {
                    'name': 'میراث اژدها: گودزیلا',
                    'imdb': 'goodzila',
                    'point': 8.6,
                    'background': '../images/One.Hundred.Years_.of_.Solitude.jpg'
                },
                {
                    'name': 'دارک',
                    'imdb': 'darck',
                    'point': 8,
                    'background': '../images/ezgif.com-webp-to-jpg-10.jpg'
                },
                {
                    'name': 'get pilot',
                    'imdb': 'get-pilot',
                    'point': 5.6,
                    'background': '../images/16554708351930220521.ZARFILM.jpg'
                },
                {
                    'name': 'landman',
                    'imdb': 'landmanlink',
                    'point': 8.3,
                    'background': '../images/cjEcqdRdPQJhYre3HUAc5538Gk8-scaled.jpg'
                },
                {
                    'name': 'silo',
                    'imdb': 'silo',
                    'point': 8.1,
                    'background': '../images/6699ce8e81fcf.jpg'
                },
            ];
            var mediaName = document.getElementById('media-name');
            var mediaImdbLink = document.getElementById('media-imdb-link');
            var mediaPoint = document.getElementById('media-point');
            var mediaBackground = document.getElementById('media-background');

            var counter = 0;
            var interval = setInterval(function () {
                if (counter == medias.length) counter = 0;
                mediaName.innerHTML = medias[counter]['name']
                mediaImdbLink.href = medias[counter]['imdb']
                mediaPoint.innerHTML = medias[counter]['point']
                mediaBackground.src = medias[counter]['background']
                ++counter;
            },
            1000
        )


{% block homead %}
                <div class="container flex mx-auto items-center mt-32 pb-28 justify-between">
                    <!-- <div class="flex"> -->
                        <div class="w-[45%] h-96 overflow-x-scroll overflow-y-hidden flex pt-4">

                            {% for media in all_media %}
                            <div class="transition duration-300 hover:scale-110 cursor-pointer group ml-8" onclick="window.location.href='../pages/detail.html'">
                                <!-- image and icons and animations -->
                                <div class="relative w-max">
                                    <img src="{{ media.media_object.baner.url }}" alt="" class="rounded-2xl transition duration-[400ms] group-hover:brightness-50 w-48 h-72 border-black border group-hover:border-amber-500 ">
                                    <div class="absolute flex top-1 right-1">
                                        {% if media.media_object.is_subtitle %}
                                        <img class="h-7 bg-black/50 rounded-full p-1" src="{% static 'images/sound-translate.png' %}" alt="" srcset="">
                                        {% endif %}
                                        {% if media.media_object.is_sound_translate %}
                                        <img class="h-7 bg-black/50 rounded-full p-1 mr-1" src="{% static 'images/subtitle.png' %}" alt="">
                                        {% endif %}
                                    </div>
                                    {% if media.media_object.online_play == '' %}
                                    <img class="absolute top-1 left-1 h-7 p-1 bg-black/50 rounded-full" src="{% static 'images/play.png' %}" alt="">
                                    {% endif %}
                                </div>
                
                                <!-- links -->
                                <div class="absolute bottom-1/2 -translate-y-1/2 opacity-0 transition-opacity duration-[400ms] group-hover:opacity-100">
                                    <div class="flex">
                                        {% for ganer in media.media_object.ganers.all %}
                                        <a class="bg-white/20 rounded-md p-1 mr-1" href="">{{ ganer }}</a>
                                        {% endfor %}
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                        <!-- </div> -->
                        <div class="grid grid-cols-8 w-[55%]">
                            <a class="" id="media-imdb-link" href="#">
                                <div class="relative col-span-1">
                                    <div class="absolute inset-0 border-2 border-amber-500 rounded-full h-24 w-24 blur-c"></div>
                                    <img class="absolute left-1/2 -translate-x-1/2 top-1/2 translate-y-1/2 z-10" src="{% static 'images/play.png' %}" alt="">
                                </div>
                            </a>
                            <div class="col-span-6"></div>
                            <a href="#" class="col-span-1 flex flex-col items-end space-y-2">
                                <p id="media-name" class="text-4xl self-center">From</p>
                                <img id="media-imdb-link" src="{% static 'images/imdb.png' %}" alt="">
                                <h6><span id="media-point" class="text-4xl">8</span><span>/10</span></h6>
                            </a>
                        </div>
                </div>
{% endblock %}




















# Models

class MainPageSerialsAd(models.Model):
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, verbose_name='سریال')
    ad_baner = models.ImageField(upload_to='images/serials/ad/', verbose_name='عکس تبلیغاتی')

    class Meta:
        verbose_name = 'سریال تبلیغاتی صفحه اصلی'
        verbose_name_plural = 'سریال های تبلیغاتی صفحه اصلی'


    def __str__(self):
        return str(self.id)


class MainPageMoviesAd(models.Model):
    movies = models.ManyToManyField(Movie, verbose_name='سینمایی ها')

    class Meta:
        verbose_name = 'سینمایی تبلیغاتی صفحه اصلی'
        verbose_name_plural = 'سینمایی های تبلیغاتی صفحه اصلی'


    def __str__(self):
        return str(self.id)














# 
    <!-- Movie dl -->
    <div class="container mx-auto">
        <div data-accordion="collapse">
            <div class="flex items-center cursor-pointer text-slate-100 bg-black " style="background-color: #000101;" data-accordion-target="#dllink" aria-expanded="true" aria-controls="dlbox">
                <div class="flex-none flex text-xl">
                    <img class="h-7 mx-2" src="../images/download.png" alt="">
                    نسخه زیرنویس فارسی چسبیده
                    <span class="bg-amber-500 mx-2 px-2 rounded-full text-base">زیرنویس</span>
                </div>
                <hr class="grow mx-3 border-gray-600">
                <span class="p-3 py-0 text-lg bg-gray-700 rounded-full">-</span>
            </div>

            <div id="dllink" class="hidden px-2 sm:px-10 mt-5">
                <div class="flex justify-between p-5 m-5 rounded-2xl bg-gray-100/5 flex-wrap">
                    <a href="#" class="p-3 flex hover:bg-amber-600 rounded-lg border duration-[400ms] border-gray-100">
                        <img class="h-7 ml-1" src="../images/downloading.png">
                        <span>دانلود با لینک مستقیم</span>
                    </a>
                    <div class="flex w-full justify-between">
                        <div class="">
                            <p class="text-gray-400/80 mb-1 hidden sm:inline">حجم</p>
                            <p>1.92GB</p>
                        </div>
                        <div class="">
                            <p class="text-gray-400/80 mb-1 hidden sm:inline">نوع زیرنویس</p>
                            <p>SoftSub</p>
                        </div>
                        <div class=" text-left">
                            <p class="text-amber-600 font-bold text-lg">BluRay1080p</p>
                            <p class="hidden sm:inline">Encoder: YIFY</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>