<h1>Самые выгодные скины на стим маркете с CSGORUN</h1>

Скрипт для поиска наиболее выгодных минимальных цен на торговой прощадке стим по отношению к цене на сайте csgo3.run

<h2>Как использовать</h2>
1. Скачайте драйвер для вашего браузера и поместите в каталог проекта: <br>
Инструкция для браузера Google Chrome: <br>
1.1. Перейдите на сайт с выбором драйвера "https://googlechromelabs.github.io/chrome-for-testing/".  <br>
1.2. Нажмите на самый верхний вариант в таблице (Stable).  <br>
1.3. Выберите в таблице chromedriver для вашей операционной системы.  <br>
1.4. Перейдите по соответствующей ссылке в таблице после чего начнётся скачивание.  <br>
1.5. После скачивания разорхивируйте драйвер.  <br>
1.6. Добавьте драйвер в папку со скриптом переименовав его в "browserdriver".  <br>
2. Пропишите команду в терминал в каталоге проекта:
```bash
pip install -r requirements.txt
```
3. Запустите скрипт, вас попросят ввести максимальную
и минимальную сумму, в пределах которой скрипт будет искать
скины на сайте csgorun. После их ввода
скрипт начнет работать.
4. Скрипт откроет окно браузера и загрузит товары.
в указанном ценовом диапазоне для всех игр.
!!Во время этого процесса окно браузера нельзя закрыть,
свернуть или изменить его размер!!. Как только все предметы будут загружены, оно автоматически закроется.
5. Далее начнётся обработка скинов, и скрипт будет
проверять их минимальную цену на торговой площадке стима.
Лучшее соотношение цен будет
записано в файле result.txt. Будет топ-20
таких скинов для каждой игры с указанием процента профита.
6. Пока скрипт работает, он будет оставлять логи в консоли,
благодаря которым вы сможете следить за процессом выполнения скрипта.
На этом все, наслаждайтесь автоматическим поиском лучших скинов :)

<h2>Важные замечания</h2>
1. Наблюдая за консолью, можно заметить, что иногда при попытке
чтобы получить минимальную цену на торговой площадке steam,
периодически будет выдаваться ошибка 419, это значит, что мы сделали
слишком много запросов за короткий промежуток времени, это нормально, скрипт
просто подождет через одну минуту, и работа продолжится. Но если скрипт
работает большое время, ошибка может не исчезнуть через минуту, что означает
что мы сделали слишком много запросов и возможность их делать была отключена на
более длительное время (примерно от получаса до пол дня). В этом случае вы можете либо
запустите скрипт позже или воспользоваться десктопным VPN, вы можете включить VPN и изменить
его сервер прямо во время работы скрипта.
2. Иногда могут попадаться слишком профитные скины
(почти всегда из Dota 2), не спешите их выводить, большинство из них
скорее всего просто очень непопулярные вещи, у которых остались только
дорогие предложения. Вряд ли вам удастся их продать.
Немногие скины из Dota 2 являются профитными и популярными.
3. Если скрипт работает нестабильно, сообщите мне об этом по электронной почте: «thekeykeyloy@gmail.com».
или в дискорд: «Cadregich», и я постараюсь исправить все проблемы в кратчайшие сроки.
Спасибо.

<h1>Best Skin Price CSGORUN</h1>

Script for getting the most profitable skin on the Steam market in relation to its price on the csgo3.run website.

<h2>How to use</h2>
1. Download the driver for your browser and place it in the project directory: <br>
Instruction for Google Chrome browser: <br>
1.1. Go to the website with the driver selection page at "https://googlechromelabs.github.io/chrome-for-testing/".  <br>
1.2. Click on the topmost option (Stable).  <br>
1.3. In the table, locate the chromedriver for your operating system.  <br>
1.4. Follow the appropriate link to start the download.  <br>
1.5. After the download is complete, unzip the driver file.  <br>
1.6. Add the driver to the folder with the script, renaming it "browserdriver". <br>
2. Enter the command in project directory:
```bash
pip install -r requirements.txt
```
3. Run the script, you will be asked to enter the maximum
and minimum amount within which the script will search
for skins on the csgorun website, after you enter them
the script will start working
4. The script will open a browser window and load products
in a specified price range for all games.
!!During this process, the window cannot be closed,
minimized, or resized!!. Once all items are loaded, it will automatically close.
5. Next, the skins will be processed, and the script will
start checking their minimum price on the Steam Market.
The best price ratios will be
recorded in the 'result.txt' file. There will be a top 20
of such skins for each game, showing the profit percentage.
6. While the script is running, it will leave logs in the console,
thanks to which you can monitor the process of the script.
That's all, enjoy the automatic search for the best skins :)

<h2>Important Notes</h2>
1. By watching the console, you may notice that sometimes when trying
to get the minimum price from the steam market,
it will periodically give an error 419, which means that we have made
too many requests in a short period of time, this is normal, the script
will just wait one minute and the work will continue. But if the script
runs for more time, the error may not go away after one minute, which means
that we made too many requests and the ability to make them was disabled for
a longer time (about half an hour to half a day). In this case, you can either
run the script later, or use desktop vpn, you can turn on vpn and change the
server right while the script is running.
2. Sometimes you may come across skins that are too profitable
(almost always from Dota 2), don’t rush to withdraw them, most
likely it’s just a very unpopular item that only has expensive
offers left. It is unlikely that you will be able to sell it. 
There are few skins from Dota 2 that are profitable and popular.
3. If the script working unstable, please let me know by email: «thekeykeyloy@gmail.com»
or in discord: «Cadregich», and I will try to fix all the problems as soon as possible.
Thanks.
