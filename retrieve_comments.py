import sys
import collections
import string
import ROOT
from gdata.youtube import service
from random_video import GenerateVideo
from gdata.service import RequestError


#--------------------------------------
def comments_generator(client, video_id):
    """
    Returns the list of video comments given the video_ID
    """
    comments_to_return = []
    try:
        comment_feed = client.GetYouTubeVideoCommentFeed(video_id=video_id)
        #print comment_feed
    # if the video has disabled comments:
    except RequestError:
        return []

    stop_comments = 1000   

    while comment_feed is not None:
        for comment in comment_feed.entry:
            print len(comments_to_return)
            if len(comments_to_return) == stop_comments: break
            comments_to_return.append(comment)
        next_link = comment_feed.GetNextLink()
        if next_link is None:
            comment_feed = None
        else:
            try:
                comment_feed = client.GetYouTubeVideoCommentFeed(next_link.href)
            except RequestError:
                comment_feed = None
        if len(comments_to_return) == stop_comments: break


    return comments_to_return
#--------------------------------------




client = service.YouTubeService()

# Define canvas, histograms, legend and set plotting details
canvas = ROOT.TCanvas('Trigger Count Canvas','Trigger Count Canvas',200,10,700,500)
h_TriggerCount_SIG = ROOT.TH1F('Trigger Word Count', 'Trigger Word Count', 8, 0, 8)
h_TriggerCount_SIG.SetLineColor(ROOT.kRed)
h_TriggerCount_BG = ROOT.TH1F('Trigger Word Count', 'Trigger Word Count', 8, 0, 8)
h_TriggerCount_BG.SetLineColor(ROOT.kBlack)
legend = ROOT.TLegend(0.6,0.7,0.9,0.9)
legend.SetBorderSize(0)
legend.AddEntry(h_TriggerCount_SIG, 'Signal', 'l')
legend.AddEntry(h_TriggerCount_BG, 'Background', 'l')

h_CapsCount_SIG = ROOT.TH1F('Caps Fraction', 'Caps Fraction', 20, 0, 1)
h_CapsCount_SIG.SetLineColor(ROOT.kRed)
h_CapsCount_BG = ROOT.TH1F('Caps Fraction', 'Caps Fraction', 20, 0, 1)
h_CapsCount_BG.SetLineColor(ROOT.kBlack)
h_CapsCount_BG.SetStats(False)
h_CapsCount_BG.GetXaxis().SetTitle('Caps Fraction')

h_PunctCount_SIG = ROOT.TH1F('Punctuation Count', 'Punctuation Count', 20, 0, 20)
h_PunctCount_SIG.SetLineColor(ROOT.kRed)
h_PunctCount_BG = ROOT.TH1F('Punctuation Count', 'Punctuation Count', 20, 0, 20)
h_PunctCount_BG.SetLineColor(ROOT.kBlack)
h_PunctCount_BG.SetStats(False)
h_PunctCount_BG.GetXaxis().SetTitle('Punctuation Count')




# Define a list of trigger words for plotting trigger word count
trigger_words = ['fuck', 'fucking', 'fuckin', 'fucker', 'fuckers', 'shit', 'bullshit', 'kill', 'rape', 'bitch', 'bitches', 'cunt', 'cunts', 'kitchen', 'sandwich', 'feminazi', 'feminazis']

count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))

#----------------------------------BACKGROUND------------------------------------------------
bg_comments = []
ncomments = 0

while ncomments < 1000:
    BG_VIDEO_ID = GenerateVideo()
    if not BG_VIDEO_ID: continue
    bg_comments += comments_generator(client, BG_VIDEO_ID)
    ncomments = len(bg_comments)
    print 'nComments is %i ' % ncomments


for comment in bg_comments:
    try:
        words = comment.content.text.split()
    except AttributeError: continue

    trigger_count = 0
    n_caps_letters = float(sum(1 for l in comment.content.text if l.isupper()))
    n_tot_letters = float(count(comment.content.text, string.ascii_letters))
    if n_tot_letters == 0:
        h_CapsCount_BG.Fill(-1)
    else:
        h_CapsCount_BG.Fill(n_caps_letters/n_tot_letters)

    n_punct_char = count(comment.content.text, string.punctuation)
    h_PunctCount_BG.Fill(n_punct_char)
    
    for word in words:
        if word.strip(string.punctuation).lower() in trigger_words:
            trigger_count += 1
    h_TriggerCount_BG.Fill(trigger_count)


#----------------------------------SIGNAL------------------------------------------------
# Signal comments: "What It Feels Like to Be a Gamergate Target", 14675 total comments 
SIG_VIDEO_ID = 'gAyncf3DBUQ'

sig_comments = []
sig_comments += comments_generator(client, SIG_VIDEO_ID)

for comment in sig_comments:
    
    n_caps_letters = float(sum(1 for l in comment.content.text if l.isupper()))
    n_tot_letters = float(count(comment.content.text, string.ascii_letters))
    if n_tot_letters == 0:
        h_CapsCount_SIG.Fill(-1)
    else:
        h_CapsCount_SIG.Fill(n_caps_letters/n_tot_letters)

    n_punct_char = count(comment.content.text, string.punctuation)
    h_PunctCount_SIG.Fill(n_punct_char)

    trigger_count = 0
    words = comment.content.text.split()
    for word in words:
        if word.strip(string.punctuation).lower() in trigger_words:
            trigger_count += 1

    h_TriggerCount_SIG.Fill(trigger_count)

h_TriggerCount_BG.SetStats(False)
h_TriggerCount_BG.GetXaxis().SetTitle('Trigger Word Count')
h_TriggerCount_BG.Scale(1./h_TriggerCount_BG.GetSumOfWeights())
h_TriggerCount_BG.Draw()
h_TriggerCount_SIG.Scale(1./h_TriggerCount_SIG.GetSumOfWeights())
h_TriggerCount_SIG.Draw('same')
legend.Draw('same')
canvas.Print('TriggerCount.png')
canvas.Clear()


legend = ROOT.TLegend(0.6,0.7,0.9,0.9)
legend.SetBorderSize(0)
legend.AddEntry(h_CapsCount_SIG, 'Signal', 'l')
legend.AddEntry(h_CapsCount_BG, 'Background', 'l')
h_CapsCount_BG.Scale(1./h_CapsCount_BG.GetSumOfWeights())
h_CapsCount_BG.Draw()
h_CapsCount_SIG.Scale(1./h_CapsCount_SIG.GetSumOfWeights())
h_CapsCount_SIG.Draw('same')
legend.Draw('same')
canvas.Print('CapsFraction.png')
canvas.Clear()

legend = ROOT.TLegend(0.6,0.7,0.9,0.9)
legend.SetBorderSize(0)
legend.AddEntry(h_PunctCount_SIG, 'Signal', 'l')
legend.AddEntry(h_PunctCount_BG, 'Background', 'l')
h_PunctCount_BG.Scale(1./h_PunctCount_BG.GetSumOfWeights())
h_PunctCount_BG.Draw()
h_PunctCount_SIG.Scale(1./h_PunctCount_SIG.GetSumOfWeights())
h_PunctCount_SIG.Draw('same')
legend.Draw('same')
canvas.Print('PunctuationCount.png')










#--------------------------------------
#def comments_generator_2(client, video_id):
#    """
#    Returns the list of video comments given the video_ID
#    """
#    comments_to_return = []
#    try:
#        comment_feed = client.GetYouTubeVideoCommentFeed(video_id=video_id)
#    # if the video has disabled comments:
#    except RequestError:
#        return []
#
#    while comment_feed is not None:
#        for comment in comment_feed.entry:
#            comments_to_return.append(comment)
#        next_link = comment_feed.GetNextLink()
#        if next_link is None:
#             comment_feed = None
#        else:
#            try:
#                comment_feed = client.GetYouTubeVideoCommentFeed(next_link.href)
#            except RequestError:
#                comment_feed = None
#
#    return comments_to_return








#print bg_comments

#BG_words_list = []
#for comment in comments:
#    #print comment.content.text
#    if comment.content.text is None: continue
#    words = comment.content.text.split()
#    
#    BG_words_list += words

#BG_words_list_cleaned = []
#for word in BG_words_list:
#    word = word.strip(string.punctuation)
#    BG_words_list_cleaned.append(word)

#BG_words_list_cleaned.sort()
#counts = collections.Counter(BG_words_list_cleaned)
#new_list = sorted(BG_words_list_cleaned, key=counts.get, reverse=True)
##print new_list




#n_sig_comments = 0
#n_sig_comments = len(sig_comments)
#SIG_words_list = []
#for comment in sig_comments:
#    if comment.content.text is None: continue
#    print comment.content.text
#    words = comment.content.text.split()
#    SIG_words_list += words
#
#SIG_words_list_cleaned = []
#for word in SIG_words_list:
#    word = word.strip(string.punctuation)
#    SIG_words_list_cleaned.append(word)
#
#counts_sig = collections.Counter(SIG_words_list_cleaned)
#new_sig_list = sorted(SIG_words_list_cleaned, key=counts_sig.get, reverse=True)
##print new_sig_list














#    if '\\' in word: continue
#    else:
#        BG_words_list_cleaned.append(word)
#print BG_words_list_cleaned

#print len(comments)
#sys.exit()



#for i, comment in enumerate(comments_generator(client, VIDEO_ID)):
#    ncomments += 1
#    author_name = comment.author[0].name.text
#    text = comment.content.text
#    print '-'*40
#    #if i > 15: break
#   # print comment.GetSelfLink()
#    #print dir(comment.extension_attributes)
#    print("{}: {}".format(author_name, text))
    

#print 'Total # of comments: {}'.format(ncomments)




