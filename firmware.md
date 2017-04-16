# Firmware notes

TODO: work on this more ;)

## SoC

Uses a GainSpan 1101MEE IoT system-on-chip.  This contains [two ARM7 processors](https://www.sparkfun.com/products/retired/10808).  In the Aria, the core Aria application logic runs on the Application Processor, and there is a second processor running WiFi.

Third-party teardown: http://pooloferrors.com/project/2015/01/10/fitbit-teardown.html

Aria uses some extra features, such as a [modified version of the Gainspan provisioning service](https://s3.amazonaws.com/site_support/uploads/document_upload/ADK-PROV-PB.pdf), and a modified OTA update process which pulls from a remote web server (rather than being uploaded locally).

## Firmware updates

Firmware updates are retrieved from `http://www.fitbit.com/scale/firmware/${VERSION}?serialNumber=${SERIAL}`.

`${SERIAL}` must be one of:

* a valid Fitbit Aria serial number (automatically provided by `/upload` if you send a request with no weight data and an old firmware version)
* `000000000000`
* `001DC9000000` (OUI corresponds to Gainspan -- who make the WiFi controller used in the Aria)
* `001DC9D05221` (hard coded in some strings)

At the time of writing, only firmware versions 33, 35, 38 and 39 can be downloaded. [Fitbit also publish some information about security updates](https://help.fitbit.com/articles/en_US/Help_article/1164).

This contains all the code which runs on the GainSpan processors.

The GainSpan EVK (available via support portal) looks like it should be able to dump firmware from the device in 128KB chunks, but this isn't tested.

## Notes

* Includes [Treck](http://www.treck.com/treck-tcp-datasheet)

## Images

### Checksums

```
$ sha256sum *
2e66bd71855914119d16b872e70f3b307685c08abfb3abc5bb8a235f769a5020  firmware-33.dat
22827f019ef69284fed36b1e16cd8a7d68bc295937d1bf5f07cdbf91e1a9a9ca  firmware-35.dat
f0a315fcfa1e5add944869628ea775934670255ac4b540a9dd87ab518c37b03f  firmware-38.dat
75038492de789cc57a3250fc1f27fcee312215601acf7d5a665668129d87cc3b  firmware-39.dat
```

### Layout

The first 0x10 bytes appear to contain the firmware versions.

Gainspan call the WiFi Firmware `wfw`, this appears around `0x3ed18` to `0x5dc7f` in firmware-39.

### Binwalk output

Mostly seems to be picking up the HTML and PNG files used in the setup process:

```
Target File:   firmware-33.dat
MD5 Checksum:  2d028f226fd8c1ce81ed73f6605b6ef1
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
109023        0x1A9DF         HTML document footer
109623        0x1AC37         HTML document header
181137        0x2C391         HTML document header
181239        0x2C3F7         HTML document footer
252179        0x3D913         Base64 standard index table
384362        0x5DD6A         PNG image, 776 x 18, 8-bit colormap, non-interlaced
384827        0x5DF3B         Zlib compressed data, best compression
386323        0x5E513         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
386898        0x5E752         Zlib compressed data, best compression
390069        0x5F3B5         PNG image, 143 x 40, 8-bit colormap, non-interlaced
391158        0x5F7F6         Zlib compressed data, best compression
392717        0x5FE0D         PNG image, 293 x 80, 8-bit colormap, non-interlaced
393582        0x6016E         Zlib compressed data, best compression
396207        0x60BAF         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
396248        0x60BD8         Zlib compressed data, best compression
396605        0x60D3D         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
396646        0x60D66         Zlib compressed data, best compression
396997        0x60EC5         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
397038        0x60EEE         Zlib compressed data, best compression
397323        0x6100B         PNG image, 776 x 18, 8-bit colormap, non-interlaced
397696        0x61180         Zlib compressed data, best compression
399117        0x6170D         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
399459        0x61863         Zlib compressed data, best compression
402253        0x6234D         PNG image, 12 x 16, 8-bit/color RGBA, non-interlaced
402294        0x62376         Zlib compressed data, best compression
402496        0x62440         HTML document header
402580        0x62494         HTML document header
405559        0x63037         HTML document footer
407002        0x635DA         HTML document header
407080        0x63628         HTML document header
457539        0x6FB43         HTML document footer


Target File:   firmware-35.dat
MD5 Checksum:  30a3bdb650b5558f3b7ce877c9bb57bd
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
109023        0x1A9DF         HTML document footer
109623        0x1AC37         HTML document header
181449        0x2C4C9         HTML document header
181551        0x2C52F         HTML document footer
252559        0x3DA8F         Base64 standard index table
384362        0x5DD6A         PNG image, 776 x 18, 8-bit colormap, non-interlaced
384827        0x5DF3B         Zlib compressed data, best compression
386323        0x5E513         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
386898        0x5E752         Zlib compressed data, best compression
390069        0x5F3B5         PNG image, 143 x 40, 8-bit colormap, non-interlaced
391158        0x5F7F6         Zlib compressed data, best compression
392717        0x5FE0D         PNG image, 293 x 80, 8-bit colormap, non-interlaced
393582        0x6016E         Zlib compressed data, best compression
396207        0x60BAF         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
396248        0x60BD8         Zlib compressed data, best compression
396605        0x60D3D         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
396646        0x60D66         Zlib compressed data, best compression
396997        0x60EC5         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
397038        0x60EEE         Zlib compressed data, best compression
397323        0x6100B         PNG image, 776 x 18, 8-bit colormap, non-interlaced
397696        0x61180         Zlib compressed data, best compression
399117        0x6170D         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
399459        0x61863         Zlib compressed data, best compression
402253        0x6234D         PNG image, 12 x 16, 8-bit/color RGBA, non-interlaced
402294        0x62376         Zlib compressed data, best compression
402496        0x62440         HTML document header
402580        0x62494         HTML document header
405559        0x63037         HTML document footer
407002        0x635DA         HTML document header
407080        0x63628         HTML document header
457539        0x6FB43         HTML document footer


Target File:   firmware-38.dat
MD5 Checksum:  ad7c2ace8e17d93e13851b2a78055228
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
109367        0x1AB37         HTML document footer
109967        0x1AD8F         HTML document header
181793        0x2C621         HTML document header
181895        0x2C687         HTML document footer
252903        0x3DBE7         Base64 standard index table
384735        0x5DEDF         HTML document header
384819        0x5DF33         HTML document header
387798        0x5EAD6         HTML document footer
390613        0x5F5D5         PNG image, 143 x 40, 8-bit colormap, non-interlaced
391702        0x5FA16         Zlib compressed data, best compression
393261        0x6002D         PNG image, 293 x 80, 8-bit colormap, non-interlaced
394126        0x6038E         Zlib compressed data, best compression
396751        0x60DCF         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
396792        0x60DF8         Zlib compressed data, best compression
397149        0x60F5D         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
397190        0x60F86         Zlib compressed data, best compression
397541        0x610E5         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
397582        0x6110E         Zlib compressed data, best compression
397867        0x6122B         PNG image, 776 x 18, 8-bit colormap, non-interlaced
398240        0x613A0         Zlib compressed data, best compression
399661        0x6192D         PNG image, 776 x 18, 8-bit colormap, non-interlaced
400126        0x61AFE         Zlib compressed data, best compression
401622        0x620D6         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
401964        0x6222C         Zlib compressed data, best compression
404758        0x62D16         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
405333        0x62F55         Zlib compressed data, best compression
408504        0x63BB8         PNG image, 12 x 16, 8-bit/color RGBA, non-interlaced
408545        0x63BE1         Zlib compressed data, best compression
408747        0x63CAB         HTML document header
408825        0x63CF9         HTML document header
459413        0x70295         HTML document footer


Target File:   firmware-39.dat
MD5 Checksum:  e9c2f47f7251faf14f2f1dd10198b160
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
109895        0x1AD47         HTML document footer
110495        0x1AF9F         HTML document header
182321        0x2C831         HTML document header
182423        0x2C897         HTML document footer
253455        0x3DE0F         Base64 standard index table
385263        0x5E0EF         HTML document header
385347        0x5E143         HTML document header
388326        0x5ECE6         HTML document footer
391141        0x5F7E5         PNG image, 143 x 40, 8-bit colormap, non-interlaced
392230        0x5FC26         Zlib compressed data, best compression
393789        0x6023D         PNG image, 293 x 80, 8-bit colormap, non-interlaced
394654        0x6059E         Zlib compressed data, best compression
397279        0x60FDF         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
397320        0x61008         Zlib compressed data, best compression
397677        0x6116D         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
397718        0x61196         Zlib compressed data, best compression
398069        0x612F5         PNG image, 21 x 16, 8-bit/color RGBA, non-interlaced
398110        0x6131E         Zlib compressed data, best compression
398395        0x6143B         PNG image, 776 x 18, 8-bit colormap, non-interlaced
398768        0x615B0         Zlib compressed data, best compression
400189        0x61B3D         PNG image, 776 x 18, 8-bit colormap, non-interlaced
400654        0x61D0E         Zlib compressed data, best compression
402150        0x622E6         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
402492        0x6243C         Zlib compressed data, best compression
405286        0x62F26         PNG image, 1548 x 36, 8-bit colormap, non-interlaced
405861        0x63165         Zlib compressed data, best compression
409032        0x63DC8         PNG image, 12 x 16, 8-bit/color RGBA, non-interlaced
409073        0x63DF1         Zlib compressed data, best compression
409275        0x63EBB         HTML document header
409353        0x63F09         HTML document header
459941        0x704A5         HTML document footer
```

Looking for opcode signatures:

```
$ binwalk -A firmware-39.dat 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
52996         0xCF04          ARM instructions, function prologue
59736         0xE958          ARM instructions, function prologue
59752         0xE968          ARM instructions, function prologue
60280         0xEB78          ARM instructions, function prologue
69752         0x11078         ARM instructions, function prologue
120384        0x1D640         ARM instructions, function prologue
257152        0x3EC80         ARM instructions, function prologue
257200        0x3ECB0         ARM instructions, function prologue
257280        0x3ED00         ARM instructions, function prologue
257584        0x3EE30         ARM instructions, function prologue
258192        0x3F090         ARM instructions, function prologue
258816        0x3F300         ARM instructions, function prologue
258940        0x3F37C         ARM instructions, function prologue
259112        0x3F428         ARM instructions, function prologue
259372        0x3F52C         ARM instructions, function prologue
259444        0x3F574         ARM instructions, function prologue
259548        0x3F5DC         ARM instructions, function prologue
259640        0x3F638         ARM instructions, function prologue
259696        0x3F670         ARM instructions, function prologue
259800        0x3F6D8         ARM instructions, function prologue
259952        0x3F770         ARM instructions, function prologue
260988        0x3FB7C         ARM instructions, function prologue
262656        0x40200         ARM instructions, function prologue
262720        0x40240         ARM instructions, function prologue
262724        0x40244         ARM instructions, function prologue
262844        0x402BC         ARM instructions, function prologue
262892        0x402EC         ARM instructions, function prologue
265044        0x40B54         ARM instructions, function prologue
267092        0x41354         ARM instructions, function prologue
267580        0x4153C         ARM instructions, function prologue
267676        0x4159C         ARM instructions, function prologue
267704        0x415B8         ARM instructions, function prologue
267800        0x41618         ARM instructions, function prologue
267916        0x4168C         ARM instructions, function prologue
267976        0x416C8         ARM instructions, function prologue
268156        0x4177C         ARM instructions, function prologue
268296        0x41808         ARM instructions, function prologue
268360        0x41848         ARM instructions, function prologue
268452        0x418A4         ARM instructions, function prologue
269396        0x41C54         ARM instructions, function prologue
269720        0x41D98         ARM instructions, function prologue
270088        0x41F08         ARM instructions, function prologue
270412        0x4204C         ARM instructions, function prologue
271376        0x42410         ARM instructions, function prologue
271936        0x42640         ARM instructions, function prologue
272140        0x4270C         ARM instructions, function prologue
272924        0x42A1C         ARM instructions, function prologue
273160        0x42B08         ARM instructions, function prologue
273484        0x42C4C         ARM instructions, function prologue
273572        0x42CA4         ARM instructions, function prologue
273672        0x42D08         ARM instructions, function prologue
273724        0x42D3C         ARM instructions, function prologue
273768        0x42D68         ARM instructions, function prologue
273816        0x42D98         ARM instructions, function prologue
273820        0x42D9C         ARM instructions, function prologue
273900        0x42DEC         ARM instructions, function prologue
273952        0x42E20         ARM instructions, function prologue
274000        0x42E50         ARM instructions, function prologue
274004        0x42E54         ARM instructions, function prologue
274144        0x42EE0         ARM instructions, function prologue
274284        0x42F6C         ARM instructions, function prologue
274328        0x42F98         ARM instructions, function prologue
274444        0x4300C         ARM instructions, function prologue
274492        0x4303C         ARM instructions, function prologue
274540        0x4306C         ARM instructions, function prologue
274588        0x4309C         ARM instructions, function prologue
274636        0x430CC         ARM instructions, function prologue
274700        0x4310C         ARM instructions, function prologue
274752        0x43140         ARM instructions, function prologue
274816        0x43180         ARM instructions, function prologue
274992        0x43230         ARM instructions, function prologue
275208        0x43308         ARM instructions, function prologue
275416        0x433D8         ARM instructions, function prologue
275556        0x43464         ARM instructions, function prologue
275988        0x43614         ARM instructions, function prologue
276428        0x437CC         ARM instructions, function prologue
276656        0x438B0         ARM instructions, function prologue
277104        0x43A70         ARM instructions, function prologue
278604        0x4404C         ARM instructions, function prologue
278760        0x440E8         ARM instructions, function prologue
279168        0x44280         ARM instructions, function prologue
279344        0x44330         ARM instructions, function prologue
279464        0x443A8         ARM instructions, function prologue
279628        0x4444C         ARM instructions, function prologue
279772        0x444DC         ARM instructions, function prologue
279920        0x44570         ARM instructions, function prologue
280060        0x445FC         ARM instructions, function prologue
280404        0x44754         ARM instructions, function prologue
280588        0x4480C         ARM instructions, function prologue
280656        0x44850         ARM instructions, function prologue
280948        0x44974         ARM instructions, function prologue
281064        0x449E8         ARM instructions, function prologue
281660        0x44C3C         ARM instructions, function prologue
281752        0x44C98         ARM instructions, function prologue
281872        0x44D10         ARM instructions, function prologue
282004        0x44D94         ARM instructions, function prologue
282144        0x44E20         ARM instructions, function prologue
282276        0x44EA4         ARM instructions, function prologue
282344        0x44EE8         ARM instructions, function prologue
282396        0x44F1C         ARM instructions, function prologue
282576        0x44FD0         ARM instructions, function prologue
282684        0x4503C         ARM instructions, function prologue
282876        0x450FC         ARM instructions, function prologue
283132        0x451FC         ARM instructions, function prologue
283356        0x452DC         ARM instructions, function prologue
283728        0x45450         ARM instructions, function prologue
284164        0x45604         ARM instructions, function prologue
284216        0x45638         ARM instructions, function prologue
284260        0x45664         ARM instructions, function prologue
285272        0x45A58         ARM instructions, function prologue
286532        0x45F44         ARM instructions, function prologue
286660        0x45FC4         ARM instructions, function prologue
287492        0x46304         ARM instructions, function prologue
287640        0x46398         ARM instructions, function prologue
287852        0x4646C         ARM instructions, function prologue
287948        0x464CC         ARM instructions, function prologue
288024        0x46518         ARM instructions, function prologue
288116        0x46574         ARM instructions, function prologue
288224        0x465E0         ARM instructions, function prologue
288632        0x46778         ARM instructions, function prologue
288900        0x46884         ARM instructions, function prologue
289284        0x46A04         ARM instructions, function prologue
289408        0x46A80         ARM instructions, function prologue
289504        0x46AE0         ARM instructions, function prologue
289924        0x46C84         ARM instructions, function prologue
290184        0x46D88         ARM instructions, function prologue
290388        0x46E54         ARM instructions, function prologue
291328        0x47200         ARM instructions, function prologue
291468        0x4728C         ARM instructions, function prologue
291924        0x47454         ARM instructions, function prologue
291980        0x4748C         ARM instructions, function prologue
292028        0x474BC         ARM instructions, function prologue
292696        0x47758         ARM instructions, function prologue
293056        0x478C0         ARM instructions, function prologue
293364        0x479F4         ARM instructions, function prologue
293476        0x47A64         ARM instructions, function prologue
293704        0x47B48         ARM instructions, function prologue
293796        0x47BA4         ARM instructions, function prologue
294068        0x47CB4         ARM instructions, function prologue
294312        0x47DA8         ARM instructions, function prologue
294456        0x47E38         ARM instructions, function prologue
294556        0x47E9C         ARM instructions, function prologue
294824        0x47FA8         ARM instructions, function prologue
295048        0x48088         ARM instructions, function prologue
295116        0x480CC         ARM instructions, function prologue
295216        0x48130         ARM instructions, function prologue
295408        0x481F0         ARM instructions, function prologue
295476        0x48234         ARM instructions, function prologue
295479        0x48237         ARMEB instructions, function prologue
295568        0x48290         ARM instructions, function prologue
295692        0x4830C         ARM instructions, function prologue
295816        0x48388         ARM instructions, function prologue
296024        0x48458         ARM instructions, function prologue
296308        0x48574         ARM instructions, function prologue
296588        0x4868C         ARM instructions, function prologue
297300        0x48954         ARM instructions, function prologue
297444        0x489E4         ARM instructions, function prologue
297704        0x48AE8         ARM instructions, function prologue
297864        0x48B88         ARM instructions, function prologue
297980        0x48BFC         ARM instructions, function prologue
298272        0x48D20         ARM instructions, function prologue
298632        0x48E88         ARM instructions, function prologue
298852        0x48F64         ARM instructions, function prologue
299320        0x49138         ARM instructions, function prologue
299420        0x4919C         ARM instructions, function prologue
299740        0x492DC         ARM instructions, function prologue
299868        0x4935C         ARM instructions, function prologue
300156        0x4947C         ARM instructions, function prologue
300208        0x494B0         ARM instructions, function prologue
300316        0x4951C         ARM instructions, function prologue
300572        0x4961C         ARM instructions, function prologue
300660        0x49674         ARM instructions, function prologue
300996        0x497C4         ARM instructions, function prologue
301316        0x49904         ARM instructions, function prologue
301444        0x49984         ARM instructions, function prologue
301912        0x49B58         ARM instructions, function prologue
302108        0x49C1C         ARM instructions, function prologue
302808        0x49ED8         ARM instructions, function prologue
303144        0x4A028         ARM instructions, function prologue
303436        0x4A14C         ARM instructions, function prologue
303700        0x4A254         ARM instructions, function prologue
304016        0x4A390         ARM instructions, function prologue
304216        0x4A458         ARM instructions, function prologue
304332        0x4A4CC         ARM instructions, function prologue
304616        0x4A5E8         ARM instructions, function prologue
304904        0x4A708         ARM instructions, function prologue
305520        0x4A970         ARM instructions, function prologue
306320        0x4AC90         ARM instructions, function prologue
306868        0x4AEB4         ARM instructions, function prologue
306972        0x4AF1C         ARM instructions, function prologue
307296        0x4B060         ARM instructions, function prologue
307352        0x4B098         ARM instructions, function prologue
308064        0x4B360         ARM instructions, function prologue
308536        0x4B538         ARM instructions, function prologue
309020        0x4B71C         ARM instructions, function prologue
309412        0x4B8A4         ARM instructions, function prologue
309516        0x4B90C         ARM instructions, function prologue
309672        0x4B9A8         ARM instructions, function prologue
309864        0x4BA68         ARM instructions, function prologue
310028        0x4BB0C         ARM instructions, function prologue
310280        0x4BC08         ARM instructions, function prologue
310396        0x4BC7C         ARM instructions, function prologue
310480        0x4BCD0         ARM instructions, function prologue
310624        0x4BD60         ARM instructions, function prologue
310680        0x4BD98         ARM instructions, function prologue
310764        0x4BDEC         ARM instructions, function prologue
310880        0x4BE60         ARM instructions, function prologue
311040        0x4BF00         ARM instructions, function prologue
311240        0x4BFC8         ARM instructions, function prologue
311516        0x4C0DC         ARM instructions, function prologue
311564        0x4C10C         ARM instructions, function prologue
311972        0x4C2A4         ARM instructions, function prologue
312028        0x4C2DC         ARM instructions, function prologue
312292        0x4C3E4         ARM instructions, function prologue
312440        0x4C478         ARM instructions, function prologue
312596        0x4C514         ARM instructions, function prologue
312840        0x4C608         ARM instructions, function prologue
312912        0x4C650         ARM instructions, function prologue
313084        0x4C6FC         ARM instructions, function prologue
313156        0x4C744         ARM instructions, function prologue
313368        0x4C818         ARM instructions, function prologue
313792        0x4C9C0         ARM instructions, function prologue
313908        0x4CA34         ARM instructions, function prologue
314092        0x4CAEC         ARM instructions, function prologue
314152        0x4CB28         ARM instructions, function prologue
314272        0x4CBA0         ARM instructions, function prologue
314508        0x4CC8C         ARM instructions, function prologue
314800        0x4CDB0         ARM instructions, function prologue
315448        0x4D038         ARM instructions, function prologue
316848        0x4D5B0         ARM instructions, function prologue
317032        0x4D668         ARM instructions, function prologue
317836        0x4D98C         ARM instructions, function prologue
318820        0x4DD64         ARM instructions, function prologue
319148        0x4DEAC         ARM instructions, function prologue
320296        0x4E328         ARM instructions, function prologue
320676        0x4E4A4         ARM instructions, function prologue
320964        0x4E5C4         ARM instructions, function prologue
321700        0x4E8A4         ARM instructions, function prologue
322928        0x4ED70         ARM instructions, function prologue
323420        0x4EF5C         ARM instructions, function prologue
323968        0x4F180         ARM instructions, function prologue
324516        0x4F3A4         ARM instructions, function prologue
324800        0x4F4C0         ARM instructions, function prologue
325804        0x4F8AC         ARM instructions, function prologue
325940        0x4F934         ARM instructions, function prologue
326004        0x4F974         ARM instructions, function prologue
326080        0x4F9C0         ARM instructions, function prologue
326252        0x4FA6C         ARM instructions, function prologue
326340        0x4FAC4         ARM instructions, function prologue
326472        0x4FB48         ARM instructions, function prologue
326584        0x4FBB8         ARM instructions, function prologue
326856        0x4FCC8         ARM instructions, function prologue
326928        0x4FD10         ARM instructions, function prologue
327184        0x4FE10         ARM instructions, function prologue
327252        0x4FE54         ARM instructions, function prologue
327376        0x4FED0         ARM instructions, function prologue
327748        0x50044         ARM instructions, function prologue
327920        0x500F0         ARM instructions, function prologue
328068        0x50184         ARM instructions, function prologue
328252        0x5023C         ARM instructions, function prologue
328312        0x50278         ARM instructions, function prologue
328408        0x502D8         ARM instructions, function prologue
328620        0x503AC         ARM instructions, function prologue
328864        0x504A0         ARM instructions, function prologue
328916        0x504D4         ARM instructions, function prologue
329088        0x50580         ARM instructions, function prologue
330636        0x50B8C         ARM instructions, function prologue
330676        0x50BB4         ARM instructions, function prologue
330988        0x50CEC         ARM instructions, function prologue
331012        0x50D04         ARM instructions, function prologue
331208        0x50DC8         ARM instructions, function prologue
331428        0x50EA4         ARM instructions, function prologue
331464        0x50EC8         ARM instructions, function prologue
331500        0x50EEC         ARM instructions, function prologue
331792        0x51010         ARM instructions, function prologue
331912        0x51088         ARM instructions, function prologue
331948        0x510AC         ARM instructions, function prologue
331984        0x510D0         ARM instructions, function prologue
332060        0x5111C         ARM instructions, function prologue
332368        0x51250         ARM instructions, function prologue
332496        0x512D0         ARM instructions, function prologue
332596        0x51334         ARM instructions, function prologue
332956        0x5149C         ARM instructions, function prologue
333140        0x51554         ARM instructions, function prologue
333632        0x51740         ARM instructions, function prologue
333936        0x51870         ARM instructions, function prologue
334496        0x51AA0         ARM instructions, function prologue
334596        0x51B04         ARM instructions, function prologue
335560        0x51EC8         ARM instructions, function prologue
335904        0x52020         ARM instructions, function prologue
336136        0x52108         ARM instructions, function prologue
336464        0x52250         ARM instructions, function prologue
336728        0x52358         ARM instructions, function prologue
336812        0x523AC         ARM instructions, function prologue
336908        0x5240C         ARM instructions, function prologue
337352        0x525C8         ARM instructions, function prologue
337656        0x526F8         ARM instructions, function prologue
337848        0x527B8         ARM instructions, function prologue
338508        0x52A4C         ARM instructions, function prologue
339000        0x52C38         ARM instructions, function prologue
339464        0x52E08         ARM instructions, function prologue
339896        0x52FB8         ARM instructions, function prologue
340180        0x530D4         ARM instructions, function prologue
340408        0x531B8         ARM instructions, function prologue
340688        0x532D0         ARM instructions, function prologue
340844        0x5336C         ARM instructions, function prologue
340948        0x533D4         ARM instructions, function prologue
341100        0x5346C         ARM instructions, function prologue
341832        0x53748         ARM instructions, function prologue
342080        0x53840         ARM instructions, function prologue
342196        0x538B4         ARM instructions, function prologue
342312        0x53928         ARM instructions, function prologue
342360        0x53958         ARM instructions, function prologue
342536        0x53A08         ARM instructions, function prologue
342836        0x53B34         ARM instructions, function prologue
342992        0x53BD0         ARM instructions, function prologue
343432        0x53D88         ARM instructions, function prologue
343916        0x53F6C         ARM instructions, function prologue
344016        0x53FD0         ARM instructions, function prologue
344080        0x54010         ARM instructions, function prologue
344188        0x5407C         ARM instructions, function prologue
344336        0x54110         ARM instructions, function prologue
344564        0x541F4         ARM instructions, function prologue
345216        0x54480         ARM instructions, function prologue
345288        0x544C8         ARM instructions, function prologue
345328        0x544F0         ARM instructions, function prologue
345528        0x545B8         ARM instructions, function prologue
345796        0x546C4         ARM instructions, function prologue
346012        0x5479C         ARM instructions, function prologue
346304        0x548C0         ARM instructions, function prologue
346436        0x54944         ARM instructions, function prologue
346496        0x54980         ARM instructions, function prologue
346588        0x549DC         ARM instructions, function prologue
346868        0x54AF4         ARM instructions, function prologue
347020        0x54B8C         ARM instructions, function prologue
347116        0x54BEC         ARM instructions, function prologue
347416        0x54D18         ARM instructions, function prologue
347596        0x54DCC         ARM instructions, function prologue
347724        0x54E4C         ARM instructions, function prologue
347832        0x54EB8         ARM instructions, function prologue
348048        0x54F90         ARM instructions, function prologue
348440        0x55118         ARM instructions, function prologue
348548        0x55184         ARM instructions, function prologue
348712        0x55228         ARM instructions, function prologue
349080        0x55398         ARM instructions, function prologue
349328        0x55490         ARM instructions, function prologue
349416        0x554E8         ARM instructions, function prologue
349540        0x55564         ARM instructions, function prologue
349616        0x555B0         ARM instructions, function prologue
349896        0x556C8         ARM instructions, function prologue
349988        0x55724         ARM instructions, function prologue
350156        0x557CC         ARM instructions, function prologue
350944        0x55AE0         ARM instructions, function prologue
351084        0x55B6C         ARM instructions, function prologue
351124        0x55B94         ARM instructions, function prologue
351396        0x55CA4         ARM instructions, function prologue
351752        0x55E08         ARM instructions, function prologue
352164        0x55FA4         ARM instructions, function prologue
352672        0x561A0         ARM instructions, function prologue
354012        0x566DC         ARM instructions, function prologue
357372        0x573FC         ARM instructions, function prologue
357980        0x5765C         ARM instructions, function prologue
358324        0x577B4         ARM instructions, function prologue
358796        0x5798C         ARM instructions, function prologue
359460        0x57C24         ARM instructions, function prologue
359912        0x57DE8         ARM instructions, function prologue
360748        0x5812C         ARM instructions, function prologue
360752        0x58130         ARM instructions, function prologue
361080        0x58278         ARM instructions, function prologue
361308        0x5835C         ARM instructions, function prologue
361476        0x58404         ARM instructions, function prologue
362840        0x58958         ARM instructions, function prologue
362868        0x58974         ARM instructions, function prologue
363524        0x58C04         ARM instructions, function prologue
363880        0x58D68         ARM instructions, function prologue
364000        0x58DE0         ARM instructions, function prologue
364380        0x58F5C         ARM instructions, function prologue
364896        0x59160         ARM instructions, function prologue
365352        0x59328         ARM instructions, function prologue
366216        0x59688         ARM instructions, function prologue
366304        0x596E0         ARM instructions, function prologue
366600        0x59808         ARM instructions, function prologue
367936        0x59D40         ARM instructions, function prologue
368140        0x59E0C         ARM instructions, function prologue
368396        0x59F0C         ARM instructions, function prologue
368708        0x5A044         ARM instructions, function prologue
369208        0x5A238         ARM instructions, function prologue
369368        0x5A2D8         ARM instructions, function prologue
369788        0x5A47C         ARM instructions, function prologue
370268        0x5A65C         ARM instructions, function prologue
370772        0x5A854         ARM instructions, function prologue
371176        0x5A9E8         ARM instructions, function prologue
372368        0x5AE90         ARM instructions, function prologue
372484        0x5AF04         ARM instructions, function prologue
373560        0x5B338         ARM instructions, function prologue
373796        0x5B424         ARM instructions, function prologue
373876        0x5B474         ARM instructions, function prologue
373960        0x5B4C8         ARM instructions, function prologue
374708        0x5B7B4         ARM instructions, function prologue
375052        0x5B90C         ARM instructions, function prologue
375252        0x5B9D4         ARM instructions, function prologue
375368        0x5BA48         ARM instructions, function prologue
375556        0x5BB04         ARM instructions, function prologue
375888        0x5BC50         ARM instructions, function prologue
```


