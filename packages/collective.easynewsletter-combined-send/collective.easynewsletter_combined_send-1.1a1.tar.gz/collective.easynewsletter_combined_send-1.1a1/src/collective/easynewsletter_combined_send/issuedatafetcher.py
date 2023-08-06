# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from plone.app.multilingual.api import get_translation_manager
from Products.EasyNewsletter.interfaces import IIssueDataFetcher
from Products.EasyNewsletter.issuedatafetcher import DefaultDXIssueDataFetcher
from zope.interface import implementer


@implementer(IIssueDataFetcher)
class CombindSendDXIssueDataFetcher(DefaultDXIssueDataFetcher):
    """
    """

    def _render_output_html(self, preview=False):
        """ Return rendered newsletter
            with header+body+footer with all translations combined (raw html)
            except when preview=True, than just render current issue.
        """
        output_html = ""
        if preview:
            output_tmpl_id = self.issue.output_template
            issue_tmpl = self.issue.restrictedTraverse(str(output_tmpl_id))
            return issue_tmpl.render()

        tlm = get_translation_manager(self.issue)
        translations = tlm.get_translations()
        # context_language = ILanguage(self.issue).get_language()
        for lang, issue in translations.items():
            output_tmpl_id = issue.output_template
            issue_tmpl = issue.restrictedTraverse(str(output_tmpl_id))
            output_html_part = issue_tmpl.render()
            if output_html:
                # only use the real content, for every additional translation
                # and insert it into body tag of first output_html_part
                # output_html_part = "test additional languages\n"
                output_html = self._merge_content(output_html, output_html_part)
            else:
                output_html = output_html_part
        return output_html

    def _merge_content(self, output_html, output_html_part):
        part_soup = BeautifulSoup(output_html_part, "html.parser")
        output_soup = BeautifulSoup(output_html, "html.parser")
        content_parts = part_soup.select("body > *")
        for part in content_parts:
            output_soup.body.append(part)
        return str(output_soup)
